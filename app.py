from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
from transformers import pipeline
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import torch
import gc
from textblob import TextBlob
import yake

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
keyword_extractor = yake.KeywordExtractor()

@lru_cache(maxsize=100)
def cached_summarize(text, max_length=130, min_length=30):
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

def process_chunks(text, chunk_size=1000):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(cached_summarize, chunks))
    return " ".join(summaries)

def safe_summarize(text, length='medium'):
    lengths = {
        'short': {'max_length': 75, 'min_length': 30},
        'medium': {'max_length': 150, 'min_length': 50},
        'long': {'max_length': 300, 'min_length': 100}
    }
    
    try:
        if len(text) > 1000:
            return process_chunks(text)
        return cached_summarize(text, **lengths[length])
    except Exception:
        return process_chunks(text, chunk_size=500)

def analyze_text(text):
    blob = TextBlob(text)
    words = text.split()
    sentences = text.split('.')
    
    # Improved keyword extraction configuration
    kw_extractor = yake.KeywordExtractor(
        lan="en", 
        n=2,                      # Extract 2-word phrases
        dedupLim=0.3,            # Higher threshold for deduplication
        dedupFunc='seqm',        # Sequence matcher for deduplication
        windowsSize=2,           # Context window size
        top=5,                   # Number of keywords to extract
        features=None
    )
    
    # Extract keywords with custom parameters
    keywords = kw_extractor.extract_keywords(text)
    key_topics = [kw[0] for kw in sorted(keywords, key=lambda x: x[1])[:5]]

    stats = {
        'sentiment': round(blob.sentiment.polarity, 2),
        'subjectivity': round(blob.sentiment.subjectivity, 2),
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_words_per_sentence': round(len(words) / len(sentences), 1),
        'key_topics': key_topics
    }
    return stats
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
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()

        if 'file' in request.files:
            file = request.files['file']
            if not file.filename.endswith('.pdf'):
                return jsonify({'error': 'Please upload a PDF file'}), 400
            text = extract_text_from_pdf(file)
        else:
            text = request.form.get('text', '')

        if len(text.split()) < 30:
            return jsonify({'error': 'Text too short to summarize'}), 400

        length = request.form.get('length', 'medium')
        summary = safe_summarize(text, length)
        stats = analyze_text(text)

        return jsonify({
            'summary': summary,
            'stats': stats
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(threaded=True)