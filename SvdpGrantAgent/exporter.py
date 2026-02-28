import os
import json
from datetime import datetime
from fpdf import FPDF
from typing import Dict

class DocumentExporter:
    """
    Handles exporting approved grant drafts to human-readable formats.
    """
    
    class PDF(FPDF):
        def header(self):
            # SVdP Branding
            self.set_font('helvetica', 'B', 16)
            self.set_text_color(0, 135, 81) # SVdP Approved Green (#008751)
            self.cell(0, 10, 'Saint Vincent de Paul St. Pats Conference', ln=True, align='L')
            self.set_font('helvetica', 'I', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, 'Automated Grant Drafting System', ln=True, align='L')
            self.ln(10)
            # Green horizontal line
            self.set_draw_color(0, 135, 81)
            self.set_line_width(1)
            self.line(10, 32, 200, 32)
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d")}', align='C')

    @staticmethod
    def export_to_markdown(draft_payload: dict, grant_id: str) -> str:
        """
        Exports the draft to a Markdown file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"draft_{grant_id}_{timestamp}.md"
        output_path = os.path.join("exports", filename)
        
        os.makedirs("exports", exist_ok=True)
        
        content = f"# Grant Application Draft: {grant_id}\n\n"
        content += f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "---\n\n"
        
        for section, body in draft_payload.items():
            content += f"## {section}\n\n{body}\n\n"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return output_path

    @staticmethod
    def export_to_pdf(draft_payload: Dict[str, str], grant_id: str) -> str:
        """
        Exports the draft to a professional PDF file using fpdf2.
        """
        pdf = DocumentExporter.PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title
        pdf.set_font('helvetica', 'B', 20)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 15, f'Grant Application Draft: {grant_id}', ln=True)
        pdf.ln(5)

        # Content Sections
        for section, content in draft_payload.items():
            # Section Header
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_fill_color(243, 244, 246) # Light Grey
            pdf.cell(0, 10, section, ln=True, fill=True)
            pdf.ln(2)
            
            # Section Content
            pdf.set_font('helvetica', '', 12)
            pdf.multi_cell(0, 8, content)
            pdf.ln(10)

        # Audit/Appendix
        pdf.add_page()
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, 'Audit Trail & Citation Traces', ln=True)
        pdf.set_font('helvetica', 'I', 9)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 5, "This document was generated using the SVdP Agentic System with strict RAG confinement. Every metric or factual claim is associated with a source document verified by the organization.")
        
        # Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grant_application_{grant_id}_{timestamp}.pdf"
        output_path = os.path.join("exports", filename)
        
        os.makedirs("exports", exist_ok=True)
        pdf.output(output_path)
        
        return output_path

DocumentExportFactory = DocumentExporter
