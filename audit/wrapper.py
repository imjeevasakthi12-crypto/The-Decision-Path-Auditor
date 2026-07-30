import hashlib
import json
from datetime import datetime
from audit.redaction import redact_text

def create_trace_payload(session_id: str, user_id: str, prompt: str, context: list, tools: list, reasoning: list, decision: str, response: str):
    redacted_prompt, mappings_1 = redact_text(prompt)
    redacted_response, mappings_2 = redact_text(response)
    redacted_decision, mappings_3 = redact_text(decision)
    
    all_mappings = mappings_1 + mappings_2 + mappings_3
    
    payload = {
        "session_id": session_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "original_prompt": redacted_prompt,
        "context_retrieved": context,
        "tools_called": tools,
        "reasoning_steps": reasoning,
        "final_decision": redacted_decision,
        "final_response": redacted_response
    }
    
    hash_input = json.dumps(payload, sort_keys=True).encode('utf-8')
    hash_value = hashlib.sha256(hash_input).hexdigest()
    
    return payload, hash_value, all_mappings
