import pickle
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "api" / "models"

class SentimentPredictor:
    def __init__(self):
        with open(MODEL_PATH / "vectorizer.pkl", "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(MODEL_PATH / "model.pkl", "rb") as f:
            self.model = pickle.load(f)
    
    def predict(self, text):
        text_vec = self.vectorizer.transform([text])
        proba = self.model.predict_proba(text_vec)[0]
        sentiment = "positive" if proba[1] > 0.5 else "negative"
        confidence = max(proba)
        return sentiment, round(confidence, 2)

if __name__ == "__main__":
    import sys
    predictor = SentimentPredictor()
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        sentiment, confidence = predictor.predict(text)
        print(f"Sentiment: {sentiment} (Confidence: {confidence})")
    else:
        print("Usage: python predict.py \"Your review text here\"")