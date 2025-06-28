

# IMDB Sentiment Analysis

A simple web app to analyze the sentiment of IMDB movie reviews using a machine learning model served with FastAPI and a modern Next.js frontend.

---

## 🚀 Frontend

- **Frontend Repository:** [IMDB Sentiment Frontend](https://github.com/AbrshS/imdb-sentiment-frontend.git)
- **Live Demo:** [https://imdb-sentiment-frontend.vercel.app/](https://imdb-sentiment-frontend.vercel.app/)

---

## 🛠️ Backend Setup

### 1. Clone the repository

```bash
git clone <your-backend-repo-url>
cd <your-backend-repo>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the model

```bash
run imdb-movie-review-analysis.ipynb
```
- This will generate `model.pkl` and `vectorizer.pkl` in the `api/models/` directory.

### 4. Run the FastAPI server

```bash
uvicorn api.app:app --reload
```
- The API will be available at `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

---

## 🧪 How to Run Predictions

You can use the `/predict` endpoint:

**Example:**
```bash
curl "http://127.0.0.1:8000/predict?text=This%20movie%20was%20fantastic"
```

**Response:**
```json
{
  "text": "This movie was fantastic",
  "sentiment": "positive",
  "confidence": 0.98,
  "success": true
}
```

---

## 🌐 Frontend

- The frontend is built with Next.js and Tailwind CSS.
- Visit the live app: [https://imdb-sentiment-frontend.vercel.app/](https://imdb-sentiment-frontend.vercel.app/)

---


## 📝 Credits

- Frontend: [IMDB Sentiment Frontend](https://imdb-sentiment-frontend.vercel.app/)
- Backend: FastAPI, scikit-learn

