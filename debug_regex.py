import re

def test_regex():
    text = "Contact me at [EMAIL_REDACTED] or 555-0199."
    # Current regex in guardrails.py
    pattern = r'(?:\+?1[-.\s]?)?(?:\(\d{3}\)[-.\s]?|\d{3}[-.\s]?)?\d{3}[-.\s]?\d{4}'
    scrubbed = re.sub(pattern, '[PHONE_REDACTED]', text)
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print(f"Scubbed: {scrubbed}")
    print(f"Success? {'[PHONE_REDACTED]' in scrubbed}")

    # Fixed regex
    pattern_fixed = r'(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}[-.\s]?\d{4}'
    scrubbed_fixed = re.sub(pattern_fixed, '[PHONE_REDACTED]', text)
    print(f"Fixed Success? {'[PHONE_REDACTED]' in scrubbed_fixed}")
    print(f"Fixed Scrubbed: {scrubbed_fixed}")

if __name__ == "__main__":
    test_regex()
