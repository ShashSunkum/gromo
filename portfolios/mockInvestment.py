import random
from datetime import datetime, timedelta
from supabase import create_client, Client

# Supabase credentials

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_valid_user_investment_id():
    """Fetch an existing user_investment_id from Supabase."""
    response = supabase.table("user_investments").select("id").limit(1).execute()
    if response.data:
        return response.data[0]["id"]
    print("No valid user_investment_id found. Ensure user_investments table has data.")
    return None

def get_unused_cashback_transaction_ids():
    """Fetch all unused cashback_transaction_id values from Supabase."""
    # Fetch all used cashback_transaction_id values in investment_transactions
    used_response = supabase.table("investment_transactions").select("cashback_transaction_id").execute()
    used_ids = {row["cashback_transaction_id"] for row in used_response.data} if used_response.data else set()

    # Fetch all available cashback_transaction_id values
    available_response = supabase.table("cashback_transactions").select("id").execute()
    available_ids = {row["id"] for row in available_response.data} if available_response.data else set()

    # Find unused cashback transaction IDs
    unused_ids = list(available_ids - used_ids)
    
    if not unused_ids:
        print("No available cashback_transaction_id found. Insert more cashback transactions.")
        return None
    
    return unused_ids

def insert_mock_data():
    """Insert mock investment transactions with valid user_investment_id and unique cashback_transaction_id."""
    user_investment_id = get_valid_user_investment_id()
    if not user_investment_id:
        print("Aborting: No valid user investment found.")
        return  # Exit if no valid user_investment_id is found

    cashback_ids = get_unused_cashback_transaction_ids()
    if not cashback_ids:
        print("Aborting: No available cashback_transaction_id found.")
        return  # Exit if no cashback transaction IDs are available

    transactions = []
    start_date = datetime.now() - timedelta(days=365)

    for _ in range(min(10, len(cashback_ids))):  # Only insert up to the available cashback IDs
        cashback_transaction_id = cashback_ids.pop(0)  # Get and remove an ID from the list

        investment_date = start_date + timedelta(days=random.randint(1, 365))
        amount_invested = round(random.uniform(100, 5000), 2)
        price_per_unit = round(random.uniform(10, 200), 2)
        units_purchased = round(amount_invested / price_per_unit, 4)

        transactions.append({
            "user_investment_id": user_investment_id,
            "cashback_transaction_id": cashback_transaction_id,
            "investment_date": investment_date.isoformat(),
            "amount_invested": amount_invested,
            "units_purchased": units_purchased,
            "price_per_unit": price_per_unit
        })

    response = supabase.table("investment_transactions").insert(transactions).execute()

    if response.data:
        print("Mock transactions inserted successfully.")
    else:
        print(f"Error inserting transactions: {response['error']}")

if __name__ == "__main__":
    insert_mock_data()
