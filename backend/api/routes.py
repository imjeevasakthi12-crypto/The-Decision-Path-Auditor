from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.postgres import get_db
from backend.models.schema import SessionLog, TokenMapping, User, Role
from audit.agent_executor import execute_agent_request
from audit.redaction import redact_text
from pydantic import BaseModel
import uuid
import hashlib
import json

router = APIRouter()

class TraceRequest(BaseModel):
    user_id: str = "DEFAULT_USER"
    prompt: str
    domain: str = "Loan Approval"
    fields: list = []

@router.post("/execute_trace")
def execute_trace(request: TraceRequest, db: Session = Depends(get_db)):
    session_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"
    
    # Ensure default user exists for DB foreign key constraint
    db_user = db.query(User).first()
    if not db_user:
        db_role = db.query(Role).filter(Role.name == "USER").first()
        if not db_role:
            db_role = Role(name="USER")
            db.add(db_role)
            db.commit()
            db.refresh(db_role)
        db_user = User(username="system_user", hashed_password="hashed_placeholder", role_id=db_role.id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # 1. Execute Domain Reasoning Agent
    final_output, intermediate_steps, risk_level = execute_agent_request(
        request.prompt, domain=request.domain, fields=request.fields
    )
    
    # 2. Redact PII from Inputs and Outputs
    redacted_prompt, mappings_1 = redact_text(request.prompt)
    redacted_response, mappings_2 = redact_text(final_output)
    
    # Convert steps to JSON string for redaction, then back
    steps_str = json.dumps(intermediate_steps)
    redacted_steps_str, mappings_3 = redact_text(steps_str)
    redacted_steps = json.loads(redacted_steps_str) if redacted_steps_str != "[REDACTION_ERROR_TEXT_REMOVED]" else []
    
    all_mappings = mappings_1 + mappings_2 + mappings_3
    
    # 3. Construct Payload & Real Cryptographic Hash
    payload = {
        "session_id": session_id,
        "user_id": request.user_id,
        "domain": request.domain,
        "original_prompt": redacted_prompt,
        "reasoning_steps": redacted_steps,
        "final_decision": redacted_response,
        "final_response": redacted_response,
        "risk_level": risk_level
    }
    
    hash_input = json.dumps(payload, sort_keys=True).encode('utf-8')
    hash_value = hashlib.sha256(hash_input).hexdigest()
    
    # 4. Store in DB
    db_log = SessionLog(
        session_id=session_id,
        user_id=db_user.id,
        original_prompt=payload["original_prompt"],
        reasoning_steps=payload["reasoning_steps"],
        final_decision=payload["final_decision"],
        final_response=payload["final_response"],
        hash_value=hash_value
    )
    db.add(db_log)
    
    for m in all_mappings:
        db_map = TokenMapping(
            token_id=m["token_id"],
            original_value=m["original_value"],
            entity_type=m.get("entity_type", "UNKNOWN")
        )
        db.add(db_map)
        
    db.commit()
    
    return {
        "message": "Trace executed and logged successfully",
        "session_id": session_id,
        "hash_value": hash_value,
        "final_decision": final_output,
        "risk_level": risk_level,
        "reasoning_steps": intermediate_steps
    }
