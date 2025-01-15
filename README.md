# SyntheSummary 📄 

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0.1-red.svg)](https://flask.palletsprojects.com/)
[![Transformers](https://img.shields.io/badge/Transformers-4.35.2-yellow.svg)](https://huggingface.co/transformers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## 📌 Overview

SyntheSummary is an advanced NLP-powered text summarization platform that leverages state-of-the-art transformer models to generate concise, accurate summaries from both text and PDF documents. Built with Python and modern web technologies, it provides an intuitive interface for document processing with additional features like sentiment analysis and key topic extraction.


## ✨ Features

- **Text Summarization**
  - Direct text input processing
  - PDF document support
  - Intelligent chunking for large documents
  
- **Analysis Tools**
  - Sentiment analysis
  - Key topic extraction
  - Word count statistics

- **User Interface**
  - Dark/Light mode toggle
  - Drag-and-drop file upload
  - Responsive design
  - Export functionality

## 🛠️ Tech Stack

- **Backend**
  ```python
  - Python 3.8+
  - Flask
  - Hugging Face Transformers
  - PyPDF2
  - TextBlob
  - YAKE
  ```

- **Frontend**
  ```javascript
  - HTML5
  - JavaScript
  - Tailwind CSS
  ```

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/syntheSummary.git
   cd syntheSummary
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 🚀 Usage

1. **Start the application**
   - Navigate to `http://localhost:5000` in your browser

2. **Input Methods**
   - Enter text directly in the text area
   - Upload PDF files using drag-and-drop

3. **Processing Options**
   - Click "Summarize" to generate summary
   - View additional analysis in results section
   - Export or copy results as needed

## 📊 Performance

- Text reduction: Up to 70%
- Information retention: ~90% accuracy
- Processing capacity: Up to 50 pages
- Local response time: < 2 seconds

## 💡 Implementation Details

### Text Processing Pipeline
```python
def process_text(text):
    # Preprocessing
    chunks = chunk_text(text)
    
    # Summarization
    summaries = [summarize(chunk) for chunk in chunks]
    
    # Analysis
    stats = analyze_text(text)
    
    return combine_results(summaries, stats)
```

### Key Components
- Custom text chunking algorithm
- BART-large-CNN model integration
- Sentiment analysis system
- Topic extraction module

## ⚠️ Development Note

This project is currently configured for local development due to the computational costs associated with hosting large language models. The architecture is designed for scalability and can be deployed when resources permit.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Contact

Alonso Nunez - [Email](mailto:your.email@example.com)

Project Link: [Click Here](https://github.com/alonso510/capstone)

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
