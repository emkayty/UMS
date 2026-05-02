"""
Transcript PDF Generation Module.
"""
import io
import uuid
from datetime import datetime
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class TranscriptPDFGenerator:
    """Generate academic transcripts in PDF."""
    
    def __init__(self, student, transcript_data):
        self.student = student
        self.data = transcript_data
        self.styles = getSampleStyleSheet()
    
    def generate(self) -> io.BytesIO:
        """Generate PDF transcript."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
            rightMargin=0.75*inch, leftMargin=0.75*inch,
            topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        
        # Header
        story.append(Paragraph(self.data.get('institution', 'UNIVERSITY'), 
            self.styles['Title']))
        story.append(Paragraph('OFFICIAL ACADEMIC TRANSCRIPT', self.styles['Heading2']))
        story.append(Spacer(1, 0.3*inch))
        
        # Student Info
        story.append(Paragraph('STUDENT INFORMATION', self.styles['Heading2']))
        user = self.student.user
        info = Table([
            ['Full Name:', f"{user.first_name} {user.last_name}"],
            ['Matric Number:', self.student.matric_number or 'N/A'],
            ['Programme:', str(self.student.programme) if self.student.programme else 'N/A'],
            ['Level:', str(self.student.current_level)],
        ], colWidths=[1.5*inch, 3*inch])
        info.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(info)
        story.append(Spacer(1, 0.3*inch))
        
        # Grades Table
        story.append(Paragraph('ACADEMIC RECORD', self.styles['Heading2']))
        headers = [['Course', 'Score', 'Grade', 'GP']]
        for c in self.data.get('courses', []):
            headers.append([c.get('code', ''), str(c.get('score', 0)), c.get('grade', ''), str(c.get('gp', 0))])
        
        if len(headers) > 1:
            tbl = Table(headers, colWidths=[2*inch, 1*inch, 1*inch, 0.8*inch])
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(tbl)
        
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"CGPA: {self.data.get('cgpa', 0.0):.2f}"))
        story.append(Paragraph(f"Verification: {str(uuid.uuid4())[:8].upper()}"))
        
        doc.build(story)
        buffer.seek(0)
        return buffer


def generate_transcript_pdf(student, data) -> io.BytesIO:
    """Generate transcript PDF."""
    return TranscriptPDFGenerator(student, data).generate()
