"""
Flag-leak protection: redact the secret token from outbound payloads.
Never log the secret token; use only in memory for sanitization.
"""

REDACTED_PLACEHOLDER = "[REDACTED]"


def sanitize_outbound(payload: str, secret_token: str) -> str:
    """
    If the payload contains the exact secret token, replace it with a placeholder.
    Ensures we never send the token to the arena (instant death).
    """
    if not secret_token or not payload:
        return payload
    if secret_token in payload:
        return payload.replace(secret_token, REDACTED_PLACEHOLDER)
    return payload
