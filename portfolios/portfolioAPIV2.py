from flask import Flask, jsonify
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from supabase import create_client, Client

app = Flask(__name__)

# -------------------------------
# Supabase Setup
# -------------------------------
# Replace these with your actual Supabase credentials or set them as environment variables.


# -------------------------------
# Yahoo Finance Data Fetching
# -------------------------------
def get_weekly_data(ticker, start_date, end_date):
    """
    Fetches weekly price data for a given ticker from Yahoo Finance between
    start_date and end_date.
    """
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'
    params = {
        'period1': int(start_date.timestamp()),
        'period2': int(end_date.timestamp()),
        'interval': '1wk',
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()['chart']['result'][0]

        timestamps = data['timestamp']
        closes = data['indicators']['quote'][0]['close']

        # Create a DataFrame of weekly dates and closing prices.
        df = pd.DataFrame({
            'Date': pd.to_datetime(timestamps, unit='s'),
            'Close': closes
        }).dropna().sort_values("Date").reset_index(drop=True)

        return df

    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

# -------------------------------
# Portfolio Endpoint
# -------------------------------
@app.route('/portfolio', methods=['GET'])
def portfolio():
    # Define the portfolio period (past 52 weeks)
    portfolio_end_date = datetime.now()
    portfolio_start_date = portfolio_end_date - timedelta(weeks=52)

    # -------------------------------
    # Fetch Transactions from Supabase
    # -------------------------------
    # Query the 'investment_transactions' table for transactions since portfolio_start_date.
    # (investment_date is stored as a timestamp in the table.)
    tx_response = supabase.table("investment_transactions") \
                          .select("*") \
                          .gte("investment_date", portfolio_start_date.isoformat()) \
                          .execute()
    transactions_data = tx_response.data

    # -------------------------------
    # Map Transactions to Ticker & Format Data
    # -------------------------------
    # (Assumption: user_investment_id maps to a ticker symbol. Adjust as needed.)
    ticker_mapping = {
        1: "VOO",
        2: "IVV",
        3: "SPY"
    }

    transactions = []
    for tx in transactions_data:
        try:
            # Convert the ISO string to a datetime object.
            tx_date = datetime.fromisoformat(tx["investment_date"])
        except Exception as ex:
            print(f"Error parsing date for transaction {tx.get('id')}: {ex}")
            continue

        ticker = ticker_mapping.get(tx["user_investment_id"])
        if not ticker:
            # If there is no mapping, skip this transaction.
            continue

        # Use the precomputed number of units purchased.
        transactions.append({
            "date": tx_date,
            "ticker": ticker,
            "units": float(tx["units_purchased"])
        })

    # -------------------------------
    # Get Price Data for Each Ticker
    # -------------------------------
    # Determine which tickers are involved.
    tickers = list({tx["ticker"] for tx in transactions})
    ticker_data = {}

    for ticker in tickers:
        df = get_weekly_data(ticker, start_date=portfolio_start_date, end_date=portfolio_end_date)
        if df is None:
            return jsonify({"error": f"Failed to fetch data for ticker {ticker}"}), 500
        ticker_data[ticker] = df

    # -------------------------------
    # Prepare Transaction Shares (Units Purchased)
    # -------------------------------
    # In our case, each transaction already includes the number of units purchased.
    transaction_shares = []
    for tx in transactions:
        tx_entry = tx.copy()
        tx_entry["shares"] = tx["units"]  # already provided by the table
        transaction_shares.append(tx_entry)

    # -------------------------------
    # Generate a Weekly Portfolio Time Series
    # -------------------------------
    # Create a list of 52 weekly dates.
    week_dates = pd.date_range(start=portfolio_start_date, end=portfolio_end_date, freq='W')
    result = []

    for week_date in week_dates:
        week_date_dt = week_date.to_pydatetime()
        # Aggregate cumulative holdings (units) for each ticker up to this week.
        holdings = {}
        for tx in transaction_shares:
            if tx["date"] <= week_date_dt:
                holdings[tx["ticker"]] = holdings.get(tx["ticker"], 0) + tx["shares"]

        # Calculate portfolio value for this week.
        portfolio_value = 0.0
        for ticker, shares in holdings.items():
            df = ticker_data[ticker]
            # Get the price on or immediately after the week_date.
            df_filtered = df[df["Date"] >= week_date_dt]
            if not df_filtered.empty:
                price = df_filtered.iloc[0]["Close"]
            else:
                # Use the last available price if the week_date is beyond the data range.
                price = df.iloc[-1]["Close"]
            portfolio_value += shares * price

        result.append({
            "x": week_date_dt.strftime("%Y-%m-%d"),
            "y": round(portfolio_value, 2),
            "holdings": {ticker: round(shares, 4) for ticker, shares in holdings.items()}
        })

    # Return the 52 weekly data points as JSON.
    return jsonify(result)

if __name__ == '__main__':
    # For development purposes; in production use a proper WSGI server.
    app.run(debug=True)
