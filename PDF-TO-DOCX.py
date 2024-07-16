import os
from PyPDF2 import PdfReader
import docx

def pdf_to_text():
    pdf_file = "livro1.pdf"
    text = ""
    with open(pdf_file, 'rb') as f:
        reader = PdfReader(f)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            text += page_text
    return text

def pdf_to_docx(output_file):
    text = pdf_to_text()
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(output_file)

# Example usage:
output_docx_file = "output_docx.docx"

pdf_to_docx(output_docx_file)