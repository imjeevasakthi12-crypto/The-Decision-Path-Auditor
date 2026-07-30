import uuid
import logging
import re

logger = logging.getLogger(__name__)

# Initialize Presidio Engines safely with fallback
analyzer = None
try:
    from presidio_analyzer import AnalyzerEngine
    analyzer = AnalyzerEngine()
except Exception as e:
    logger.warning(f"Presidio AnalyzerEngine initialization warning: {str(e)}")
    analyzer = None

PII_ENTITIES = ["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "CREDIT_CARD", "IN_PAN", "IN_AADHAAR"]

def fallback_regex_redact(text: str):
    """Fallback regex redaction when Presidio model is unavailable."""
    mappings = []
    redacted = text

    # Email regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    for match in re.finditer(email_pattern, text):
        original = match.group(0)
        token = f"<TOKEN_EMAIL_{uuid.uuid4().hex[:6].upper()}>"
        redacted = redacted.replace(original, token)
        mappings.append({"token_id": token, "original_value": original, "entity_type": "EMAIL_ADDRESS"})

    # Phone regex
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
    for match in re.finditer(phone_pattern, text):
        original = match.group(0)
        token = f"<TOKEN_PHONE_{uuid.uuid4().hex[:6].upper()}>"
        redacted = redacted.replace(original, token)
        mappings.append({"token_id": token, "original_value": original, "entity_type": "PHONE_NUMBER"})

    return redacted, mappings

def redact_text(text: str):
    """
    Scans text using Microsoft Presidio (or fallback regex), 
    replaces PII with tokens, and returns (redacted_text, token_mappings).
    """
    if not text:
        return text, []

    if analyzer is None:
        return fallback_regex_redact(text)

    try:
        results = analyzer.analyze(text=text, entities=PII_ENTITIES, language='en')
        results = sorted(results, key=lambda x: x.start, reverse=True)
        
        redacted = text
        mappings = []
        
        for res in results:
            original_val = text[res.start:res.end]
            token = f"<TOKEN_{res.entity_type}_{uuid.uuid4().hex[:6].upper()}>"
            redacted = redacted[:res.start] + token + redacted[res.end:]
            mappings.append({
                "token_id": token,
                "original_value": original_val,
                "entity_type": res.entity_type
            })
            
        return redacted, mappings
        
    except Exception as e:
        logger.error(f"Redaction failed: {str(e)}. Using fallback regex.")
        try:
            return fallback_regex_redact(text)
        except Exception:
            return "[REDACTION_ERROR_TEXT_REMOVED]", []
