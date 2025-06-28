from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pickle
import numpy as np
from pathlib import Path

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost:3000",           # Local development
    "https://localhost:3000",          # Secure local development
    "https://imdb-sentiment-frontend.vercel.app"  # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],  # Be specific about allowed methods
    allow_headers=["Content-Type", "Accept", "Origin"],  # Be specific about allowed headers
    expose_headers=["Content-Type"]  # Expose necessary headers
)

# Load models
MODEL_PATH = Path(__file__).parent / "models"

try:
    with open(MODEL_PATH / "vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    with open(MODEL_PATH / "model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {str(e)}")
    # Initialize empty models - this will cause the endpoints to return errors
    # but at least the server will start
    vectorizer = None
    model = None

@app.get("/predict")
async def predict_sentiment(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if vectorizer is None or model is None:
        raise HTTPException(
            status_code=503,
            detail="Model files not loaded. Please check server logs."
        )
    
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {
        "status": "healthy",
        "models_loaded": vectorizer is not None and model is not None
    }