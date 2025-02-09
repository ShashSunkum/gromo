import random
from datetime import datetime, timedelta
from supabase import create_client, Client

# Supabase credentials

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_mock_user_investment():
    """Insert a mock user investment and return its ID."""
    data = {
        "credit_card_id": 4,  # Ensure this exists in `credit_cards`
        "portfolio_id": 1,  # Ensure this exists in `portfolios`
        "initial_investment_date": (datetime.now() - timedelta(days=365)).isoformat(),
        "total_invested_amount": 10000.00,
        "total_units": 100.0000,
        "total_current_value": 11000.00,
        "total_growth_percentage": 10.00,
        "investment_data_points": {"history": []},
        "last_investment_date": datetime.now().isoformat()
    }
    response = supabase.table("user_investments").insert(data).execute()
    
    if response.data:
        return response.data[0]["id"]  # Return the inserted ID
    else:
        print(f"Error inserting user investment: {response['error']}")
        return None

user_investment_id = insert_mock_user_investment()
print(f"Inserted mock user_investment_id: {user_investment_id}")
