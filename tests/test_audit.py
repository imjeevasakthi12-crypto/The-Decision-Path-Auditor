import pytest
from fastapi.testclient import TestClient
from backend.main import app
from audit.redaction import redact_text
from audit.agent_executor import execute_agent_request

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_pii_redaction():
    text = "Contact John Doe at john.doe@example.com or call 555-123-4567."
    redacted, mappings = redact_text(text)
    assert "john.doe@example.com" not in redacted
    assert len(mappings) > 0

def test_agent_execution():
    decision, steps, risk = execute_agent_request("Approve loan for applicant with score 750", domain="Loan Approval")
    assert decision in ["APPROVED", "REJECTED"]
    assert len(steps) == 4
    assert risk in ["LOW", "HIGH", "MEDIUM"]

def test_execute_trace_api():
    payload = {
        "user_id": "TEST_USER_101",
        "prompt": "Evaluate loan for John Doe at john@test.com",
        "domain": "Loan Approval",
        "fields": [["Customer Name", "John Doe"], ["Credit Score", "720"]]
    }
    response = client.post("/api/agent/execute_trace", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "hash_value" in data
    assert data["session_id"].startswith("DEC-")
