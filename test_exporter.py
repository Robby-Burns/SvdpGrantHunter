import os
import pytest
from SvdpGrantAgent.exporter import DocumentExporter

def test_export_to_pdf_creates_file():
    """
    Verifies that the PDF exporter actually creates a file in the exports/ directory.
    """
    sample_payload = {
        "Mission Statement": "Test mission content.",
        "Financial Need": "Test financial content."
    }
    grant_id = "TEST_G123"
    
    # Run export
    output_path = DocumentExporter.export_to_pdf(sample_payload, grant_id)
    
    # Verify file exists
    assert os.path.exists(output_path)
    assert output_path.endswith(".pdf")
    
    # Cleanup (optional, but good for local tests)
    # os.remove(output_path)

def test_export_to_markdown_creates_file():
    """
    Verifies that the Markdown exporter creates a file.
    """
    sample_payload = {"Section": "Content"}
    grant_id = "TEST_MD"
    
    output_path = DocumentExporter.export_to_markdown(sample_payload, grant_id)
    
    assert os.path.exists(output_path)
    assert output_path.endswith(".md")
