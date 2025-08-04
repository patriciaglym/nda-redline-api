from flask import Flask, request, send_file
from docx import Document
import difflib
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ NDA Redline API is running."

@app.route('/compare-nda', methods=['POST'])
def compare_nda():
    file1 = request.files['template']
    file2 = request.files['counterparty']

    def get_text(file):
        doc = Document(file)
        return [p.text for p in doc.paragraphs if p.text.strip()]

    t_text = get_text(file1)
    c_text = get_text(file2)

    diff = difflib.HtmlDiff().make_file(t_text, c_text, fromdesc='Template NDA', todesc='Counterparty NDA')

    redlined = Document()
    redlined.add_paragraph("Redlined NDA Comparison")
    for line in diff.splitlines():
        if line.strip():
            redlined.add_paragraph(line)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    redlined.save(temp.name)
    return send_file(temp.name, as_attachment=True)
