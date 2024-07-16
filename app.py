from flask import Flask, request, send_file, render_template
import os
from PyPDF2 import PdfReader
import docx
import tempfile

app = Flask(__name__)

def pdf_to_text(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as f:
        reader = PdfReader(f)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            text += page_text
    return text

def pdf_to_docx(pdf_file, output_file):
    text = pdf_to_text(pdf_file)
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(output_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.endswith('.pdf'):
        temp_pdf = tempfile.NamedTemporaryFile(delete=False)
        temp_pdf.write(file.read())
        temp_pdf.close()
        temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        pdf_to_docx(temp_pdf.name, temp_docx.name)
        os.remove(temp_pdf.name)
        return send_file(temp_docx.name, as_attachment=True, download_name='output_docx.docx')
    return "Invalid file type"

if __name__ == '__main__':
    app.run(debug=True)
