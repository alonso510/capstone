# app.py
from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)
app.debug = True

# Initialize the summarizer
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1  # Force CPU usage
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        text = request.form.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400

        # Generate summary
        result = summarizer(text, max_length=130, min_length=30, do_sample=False)
        summary = result[0]['summary_text']
        
        return jsonify({'summary': summary})

    except Exception as e:
        print(f"Error: {str(e)}")  # This will show in your terminal
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)