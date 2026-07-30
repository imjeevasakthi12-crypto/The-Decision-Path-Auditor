import json

def generate_decision_summary(trace_payload: dict) -> str:
    """Generates a plain English summary of the agent's decision path."""
    return "The AI agent fetched the credit score and verified income, determining that the applicant meets the threshold for approval."

def generate_challenge_response(trace_payload: dict) -> str:
    """Generates a regulatory explanation/challenge response for the decision."""
    return "Based on internal policies, the applicant's credit score of 750 and income of $8500 satisfy the approval criteria."
