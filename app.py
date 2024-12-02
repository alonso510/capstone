from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
from transformers import pipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        if 'file' in request.files:
            file = request.files['file']
            if not file.filename.endswith('.pdf'):
                return jsonify({'error': 'Please upload a PDF file'}), 400
            text = extract_text_from_pdf(file)
        else:
            text = request.form.get('text', '')

        if len(text.split()) < 30:
            return jsonify({'error': 'Text too short to summarize'}), 400

        max_length = min(130, len(text.split()) // 2)
        min_length = min(30, max_length - 10)
        
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return jsonify({'summary': summary[0]['summary_text']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)