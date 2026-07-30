from langchain.tools import tool
import random

@tool
def get_credit_score(user_id: str) -> int:
    """Fetches the credit score for a given User ID. Returns an integer between 300 and 850."""
    # Dummy implementation for demo purposes
    random.seed(user_id)
    return random.randint(550, 800)

@tool
def verify_income(user_id: str) -> int:
    """Fetches the verified monthly income in USD for a given User ID."""
    random.seed(user_id + "income")
    return random.randint(3000, 12000)
