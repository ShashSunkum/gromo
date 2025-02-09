# 💸 Gromo: Put Your Lazy Money to Work

## Turn your credit card cashback into smart investments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.x-blue.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.x-purple.svg)](https://vitejs.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)](https://flask.palletsprojects.com/)

<div align="center">
  <img src="logo_name.png" alt="Gromo Logo" width="200" style="border-radius: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</div>

> Gromo revolutionizes the way you handle credit card cashback. Don't let your rewards sit idle – invest them for long-term growth!

<div align="center">

[Overview](#-overview) •
[Features](#-key-features) •
[How It Works](#-how-it-works) •
[Tech Stack](#-tech-stack) •
[Getting Started](#-getting-started)

</div>

## 🚀 Overview

Gromo is a proof-of-concept cashback investment platform that automates the process of investing your credit card rewards. By putting your "lazy money" to work, Gromo helps you maximize the potential of your cashback through smart, diversified investments in ETFs and other long-term options.

### The Problem
- Unused or underutilized credit card cashback rewards
- Lack of easy options to invest small, regular cashback amounts
- Missed opportunities for long-term growth of reward money

### Our Solution
- Automated cashback tracking and investment
- Diversified investment options based on risk preference
- Real-time performance tracking and portfolio management

## 🌟 Key Features

### 1. Smart Transaction Logging
- Automatic purchase logging from partner websites
- Dynamic cashback calculation for each transaction

### 2. Flexible Investment Options
- Manual investment of cashback rewards
- Automated monthly investment based on portfolio performance
- Risk-based portfolio selection

### 3. Real-time Performance Tracking
- Monitor investment performance metrics
- View current stock value and number of shares
- Track today's return and total return

### 4. Credit Card Management
- Track balances and available credit
- Monitor cashback rewards accumulation

## 🔄 How It Works

1. **Connect Your Card**: Link your credit card to start tracking cashback.
2. **Earn Cashback**: Make purchases and accumulate rewards.
3. **Choose Your Strategy**: Opt for manual or automated investments.
4. **Invest & Grow**: Watch your cashback turn into long-term investments.
5. **Track Performance**: Monitor your portfolio's growth in real-time.

<div align="center">
  <img src="path_to_process_flow_image" alt="Gromo Process" width="800" style="border-radius: 30px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 20px 0;" />
</div>

## 💻 Tech Stack

<div align="center">

### Frontend
![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react)
![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=for-the-badge&logo=vite)

### Backend
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Latest-red?style=for-the-badge)

### Database
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=for-the-badge&logo=postgresql)
![Supabase](https://img.shields.io/badge/Supabase-Hosting-3ECF8E?style=for-the-badge&logo=supabase)

</div>



## System Architecture
Application Layers
Frontend (React + Vite)

## User interface providing:

- Credit card and transaction summaries
- Manual investment controls
- Investment performance dashboards

### Backend (Flask)

RESTful API endpoints for:

- Transaction and cashback processing
- Credit card data management
- Investment processing (manual and automatic)
- Performance metric calculations

### Database (PostgreSQL/Supabase)
- Stores all application data including:

- Credit card information
- Transactions and cashback
- Investment records
- Portfolio configurations
- Stock data

## Data Flow

- Transaction Processing

- Records new purchases
- Calculates and stores cashback
- Updates credit card balances


## Investment Processing

- Manual: User-initiated investment into selected portfolio
- Automatic: Monthly investment based on portfolio performance
Stock allocation based on portfolio weights


## Performance Tracking

- Real-time stock price updates
- Return calculations
- Portfolio valuation



## Database Schema

- credit_cards
Stores credit card summary data.

CREATE TABLE credit_cards (
    id SERIAL PRIMARY KEY,
    cc_number VARCHAR(20) NOT NULL,
    credit_line NUMERIC(10,2) NOT NULL,
    available_credit NUMERIC(10,2) NOT NULL DEFAULT 0,
    current_balance NUMERIC(10,2) NOT NULL DEFAULT 0,
    rewards_cash NUMERIC(10,2) NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Purpose: Holds the current status of the credit card. All transactions and investments are associated with this single record.

- transactions
Logs every checkout transaction.
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    credit_card_id INTEGER NOT NULL,  -- Foreign key to credit_cards
    cc_number VARCHAR(20) NOT NULL,     -- Redundant copy for convenience
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_amount NUMERIC(10,2) NOT NULL,
    description TEXT,
    FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id)
);

Purpose: Records purchase transactions for later processing.

- cashback_transactions
Stores the cashback amount computed for each transaction.
CREATE TABLE cashback_transactions (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER NOT NULL,  -- Foreign key to transactions
    cashback_amount NUMERIC(10,2) NOT NULL DEFAULT 0,
    transaction_amount NUMERIC(10,2) NOT NULL,  -- Mirrors transaction amount
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

Purpose: Separates the cashback logic from the transaction record to allow dynamic changes in cashback rules.

- investments
Records each investment event.
CREATE TABLE investments (
    id SERIAL PRIMARY KEY,
    credit_card_id INTEGER NOT NULL,  -- Foreign key to credit_cards
    investment_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    investment_amount NUMERIC(10,2) NOT NULL,
    portfolio VARCHAR(100) NOT NULL,  -- Name of the chosen portfolio
    FOREIGN KEY (credit_card_id) REFERENCES credit_cards(id)
);
Purpose: Logs the total amount invested in a given action along with the portfolio selected.
Investment Management Tables

- portfolios
Stores metadata about available portfolios.

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    historical_return NUMERIC(5,2),  -- Average historical return (percentage)
    risk_level VARCHAR(50),          -- e.g., 'Low', 'Medium', 'High'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Purpose: Defines investment options and tracks their historical performance.

- stocks
Stores details for individual stocks.

CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100),
    current_price NUMERIC(10,2) NOT NULL DEFAULT 0,
    previous_close NUMERIC(10,2) NOT NULL DEFAULT 0,  -- Used for calculating today's return
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Purpose: Contains stock pricing data, updated periodically via external APIs.

- portfolio_stocks
Maps stocks to portfolios with defined allocation weights.

CREATE TABLE portfolio_stocks (
    id SERIAL PRIMARY KEY,
    portfolio_id INTEGER NOT NULL,  -- Foreign key to portfolios
    stock_id INTEGER NOT NULL,      -- Foreign key to stocks
    weight NUMERIC(5,2) NOT NULL,     -- Percentage weight (e.g., 20.00 means 20%)
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

Purpose: Specifies how much of an investment should be allocated to each stock within a portfolio.

- investment_details
Breaks down each investment into individual stock positions.

CREATE TABLE investment_details (
    id SERIAL PRIMARY KEY,
    investment_id INTEGER NOT NULL,  -- Foreign key to investments
    stock_id INTEGER NOT NULL,       -- Foreign key to stocks
    units NUMERIC(10,4) NOT NULL,      -- Number of shares purchased
    purchase_price NUMERIC(10,2) NOT NULL,  -- Stock price at purchase
    FOREIGN KEY (investment_id) REFERENCES investments(id),
    FOREIGN KEY (stock_id) REFERENCES stocks(id)
);

Purpose: Records the detailed allocation of an investment across various stocks.


## API Endpoints


### Investment Section
Investment Endpoints
1. Manual Investment
Create a new investment using available cashback rewards.
POST /api/invest
Request Body:
jsonCopy{
    "amount": "50.00",
    "portfolio": "Tech Growth"
}
Success Response (200 OK):
jsonCopy{
    "message": "Investment completed",
    "portfolio": "Tech Growth",
    "amount_invested": "50.00",
    "allocations": [
        {
            "stock_symbol": "AAPL",
            "units": "0.2500",
            "amount_allocated": "25.00"
        },
        {
            "stock_symbol": "GOOGL",
            "units": "0.1500",
            "amount_allocated": "15.00"
        }
    ]
}
Error Responses:

400 Bad Request: Invalid input data
404 Not Found: Portfolio not found
500 Internal Server Error: Processing failed

2. Automatic Investment
Automatically invest all available cashback into the best-performing portfolio.
CopyPOST /api/auto_invest
Success Response (200 OK):
jsonCopy{
    "message": "Auto-investment completed",
    "portfolio": "Tech Growth",
    "amount_invested": "150.00",
    "allocations": [
        {
            "stock_symbol": "AAPL",
            "units": "0.7500",
            "amount_allocated": "75.00"
        },
        {
            "stock_symbol": "GOOGL",
            "units": "0.4500",
            "amount_allocated": "45.00"
        }
    ]
}
Error Responses:

400 Bad Request: No cashback available
404 Not Found: No portfolio or credit card found
500 Internal Server Error: Processing failed

3. Investment Summary
Get a summary of all investments and their current values.
GET /api/investment_summary
Success Response (200 OK):
jsonCopy[
    {
        "investment_id": 1,
        "investment_date": "2025-02-08T18:16:01Z",
        "portfolio": "Tech Growth",
        "investment_amount": "50.00",
        "current_value": "52.50",
        "allocations": [
            {
                "stock_symbol": "AAPL",
                "units": "0.2500",
                "purchase_price": "100.00",
                "current_price": "105.00",
                "current_value": "26.25"
            },
            {
                "stock_symbol": "GOOGL",
                "units": "0.1500",
                "purchase_price": "150.00",
                "current_price": "155.00",
                "current_value": "23.25"
            }
        ]
    }
]
Error Response:

500 Internal Server Error: Failed to fetch data

4. Available Portfolios
Get list of available investment portfolios.
CopyGET /api/portfolios
Success Response (200 OK):
jsonCopy[
    {
        "id": 4,
        "name": "Tech Growth",
        "description": "High-growth technology stocks",
        "historical_return": "15.50",
        "risk_level": "High",
        "stocks": [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "weight": "40.00"
            },
            {
                "symbol": "GOOGL",
                "name": "Alphabet Inc.",
                "weight": "35.00"
            }
        ]
    }
]
Error Response:

500 Internal Server Error: Failed to fetch portfolios

5. Performance Metrics
Get real-time performance metrics for investments.
GET /api/investment_performance
Success Response (200 OK):
jsonCopy[
    {
        "investment_detail_id": 1,
        "stock_symbol": "AAPL",
        "units": "0.2500",
        "purchase_price": "100.00",
        "current_price": "105.00",
        "current_value": "26.25",
        "total_return": "1.25",
        "todays_return": "0.50"
    }
]
Error Response:

500 Internal Server Error: Failed to fetch performance data

Example cURL Commands
Manual Investment:
bashCopycurl -X POST http://localhost:5000/api/invest \
  -H "Content-Type: application/json" \
  -H "apikey: your-supabase-key" \
  -d '{
    "amount": "50.00",
    "portfolio": "Tech Growth"
  }'
Auto-Investment:
bashCopycurl -X POST http://localhost:5000/api/auto_invest \
  -H "apikey: your-supabase-key"
Get Investment Summary:
bashCopycurl http://localhost:5000/api/investment_summary \
  -H "apikey: your-supabase-key"
Get Available Portfolios:
bashCopycurl http://localhost:5000/api/portfolios \
  -H "apikey: your-supabase-key"
Get Performance Metrics:
bashCopycurl http://localhost:5000/api/investment_performance \
  -H "apikey: your-supabase-key"




## Future Enhancements

- Integration with public stock market APIs
- Multi-user support with authentication
- Advanced scheduling for automated investments
- Enhanced reporting and analytics
- Mobile application support
- Real-time transaction notifications
- Advanced portfolio rebalancing features
