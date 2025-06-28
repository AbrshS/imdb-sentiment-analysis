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

// ... existing code ...