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
    "http://localhost:8000",           # Alternative local port
    "https://localhost:3000",          # Secure local development
    "https://imdb-sentiment-frontend.vercel.app"  # Production frontend (update this)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Load models
MODEL_PATH = Path(__file__).parent / "models"

with open(MODEL_PATH / "vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open(MODEL_PATH / "model.pkl", "rb") as f:
    model = pickle.load(f)

@app.get("/predict")
async def predict_sentiment(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        text_vec = vectorizer.transform([text])
        proba = model.predict_proba(text_vec)[0]
        sentiment = "positive" if proba[1] > 0.5 else "negative"
        confidence = float(np.max(proba))
        
        return JSONResponse(
            content={
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence,
                "success": True
            },
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return JSONResponse(
        content={"status": "healthy"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )