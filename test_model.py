# test_model.py
from transformers import pipeline

def test_model():
    try:
        # Try to initialize the model
        summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1
        )
        
        # Test with a simple string
        test_text = "This is a test sentence to verify the summarization model is working correctly. It should be able to process this text without any issues."
        result = summarizer(test_text, max_length=50, min_length=10)
        
        print("Model initialized successfully!")
        print("Test summary:", result[0]['summary_text'])
        return True
        
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        return False

if __name__ == "__main__":
    test_model()