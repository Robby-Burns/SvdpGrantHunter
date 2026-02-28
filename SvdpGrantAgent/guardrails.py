import re

class Guardrails:
    """
    Implements risk guardrails specified in AgentSpec.md.txt (PII scrubbing, Sanitization).
    """
    @staticmethod
    def scrub_pii(text: str) -> str:
        """
        Simple regex-based PII scrubbing for names, emails, and phones.
        In production, use a dedicated library like Presidio or a small LLM.
        """
        # Scrub Emails
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REDACTED]', text)
        # Scrub Phone Numbers (US: 10/11-digit or 7-digit)
        # Matches formats like: +1 555-555-0199, (555) 555-0199, 555-555-0199, 555-0199
        phone_pattern = r'(?:\+?1[-.\s]?)?(?:\(\d{3}\)[-.\s]?|\d{3}[-.\s]?)\d{3}[-.\s]?\d{4}|\d{3}[-.\s]?\d{4}'
        text = re.sub(phone_pattern, '[PHONE_REDACTED]', text)
        # Scrub likely names (very basic placeholder - usually requires NER)
        # For this MVP, we focus on obvious structured PII.
        return text

    @staticmethod
    def sanitize_html(html_content: str) -> str:
        """
        Prevents prompt injection by stripping hazardous tags or script patterns.
        """
        # Basic sanitization: strip script tags and common injection patterns
        sanitized = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)
        sanitized = re.sub(r'on\w+=".*?"', '', sanitized) # strip event handlers
        return sanitized
