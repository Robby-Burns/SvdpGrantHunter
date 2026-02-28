import unittest
from SvdpGrantAgent.schema import GrantRecord, GrantStatus
from SvdpGrantAgent.scout import GenericScraper
from SvdpGrantAgent.guardrails import Guardrails

class TestSvdpGrantAgent(unittest.TestCase):
    def test_grant_record_creation(self):
        grant = GrantRecord(
            grant_id="test_123", 
            grant_source_url="http://test.com"
        )
        self.assertEqual(grant.status, GrantStatus.SCOUTED)
        self.assertEqual(grant.grant_id, "test_123")

    def test_pii_scrubbing(self):
        text = "Contact me at test@example.com or 555-0199."
        scrubbed = Guardrails.scrub_pii(text)
        self.assertIn("[EMAIL_REDACTED]", scrubbed)
        self.assertIn("[PHONE_REDACTED]", scrubbed)

    def test_html_sanitization(self):
        html = "<div>Hello<script>alert('xss')</script></div>"
        sanitized = Guardrails.sanitize_html(html)
        self.assertNotIn("<script>", sanitized)

if __name__ == "__main__":
    unittest.main()
