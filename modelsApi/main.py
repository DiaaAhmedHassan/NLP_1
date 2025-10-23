from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from n_gram import lm, load_trained_model

# Initialize FastAPI app
app = FastAPI(
    title="Bigram Language Model API",
    description="API for predicting next words using a trained bigram model",
    version="1.0.0"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Request model
class PredictionRequest(BaseModel):
    sentence: str
    top_k: Optional[int] = 5

# Response model
class WordPrediction(BaseModel):
    word: str
    probability: float

class PredictionResponse(BaseModel):
    previous_word: str
    predictions: List[WordPrediction]

# Load model on startup
@app.on_event("startup")
async def startup_event():
    load_trained_model("n_gram_model.pkl")

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Bigram Language Model API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "vocab_size": len(lm.vocab)}

# Prediction endpoint
@app.post("/predict-next", response_model=PredictionResponse)
async def predict_next_word(request: PredictionRequest):
    try:
        # Simple tokenization (you might want to use the same tokenizer as during training)
        tokens = request.sentence.strip().split()
        
        if not tokens:
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        # Get the last word as previous word
        previous_word = tokens[-1].lower()  # Convert to lowercase for consistency
        
        # Predict next words
        predictions = lm.predict_next_word(previous_word, request.top_k)
        
        # Format response
        formatted_predictions = [
            WordPrediction(word=word, probability=prob) 
            for word, prob in predictions
        ]
        
        return PredictionResponse(
            previous_word=previous_word,
            predictions=formatted_predictions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Endpoint to get sentence completion suggestions
@app.post("/complete-sentence")
async def complete_sentence(request: PredictionRequest):
    """Generate multiple completion suggestions for a sentence"""
    try:
        tokens = request.sentence.strip().split()
        
        if not tokens:
            raise HTTPException(status_code=400, detail="Sentence cannot be empty")
        
        previous_word = tokens[-1].lower()
        predictions = lm.predict_next_word(previous_word, request.top_k)
        
        completions = []
        for word, prob in predictions:
            completed_sentence = request.sentence + " " + word
            completions.append({
                "completion": completed_sentence,
                "next_word": word,
                "probability": prob
            })
        
        return {
            "original_sentence": request.sentence,
            "completions": completions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Completion error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)