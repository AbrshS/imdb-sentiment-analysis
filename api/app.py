from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
from pathlib import Path

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
MODEL_PATH = Path(__file__).parent / "models"

with open(MODEL_PATH / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_PATH / "model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/predict")
async def predict_sentiment(text: str):
    text_vec = vectorizer.transform([text])
    proba = model.predict_proba(text_vec)[0]
    sentiment = "positive" if proba[1] > 0.5 else "negative"
    confidence = float(np.max(proba))
    
    return {
        "text": text,
        "sentiment": sentiment,
        "confidence": confidence,
        "success": True
    }

@app.get("/")
async def health_check():
    return {"status": "healthy"}