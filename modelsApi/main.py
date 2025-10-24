from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import re
from collections import Counter
import pickle

from n_gram import lm, load_trained_model
from naive_bays import nb_model, load_naive_bayes_model
from log_reg import lr_model, load_logistic_regression_model

app = FastAPI(
    title="Multi-Model API",
    description="API for N-gram, Naive Bayes, and Logistic Regression models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    sentence: str
    top_k: Optional[int] = 5
    model_type: str = "n_gram"  # "n_gram", "naive_bayes", or "logistic_regression"

class WordPrediction(BaseModel):
    word: str
    probability: float

class SpamPrediction(BaseModel):
    classification: str  # "Ham" or "Spam"
    confidence: float
    probabilities: dict

class PredictionResponse(BaseModel):
    model_used: str
    previous_word: Optional[str] = None
    predictions: Optional[List[WordPrediction]] = None
    spam_prediction: Optional[SpamPrediction] = None

# Global bigram vocabulary (loaded from training)
bigram_vocab = None

def tokenize(text):
    """Simple tokenization function - SAME AS USED DURING TRAINING"""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

def load_bigram_vocab(vocab_path="bigram_vocab.pkl"):
    """Load the bigram vocabulary used during training"""
    global bigram_vocab
    try:
        with open(vocab_path, "rb") as f:
            bigram_vocab = pickle.load(f)
        print(f"✓ Bigram vocabulary loaded. Size: {len(bigram_vocab)}")
    except Exception as e:
        print(f"✗ Failed to load bigram vocabulary: {e}")
        bigram_vocab = {}

def extract_features(text):
    """
    Extract bigram features for Logistic Regression.
    This matches EXACTLY how features were extracted during training.
    """
    global bigram_vocab
    
    if bigram_vocab is None:
        raise ValueError("Bigram vocabulary not loaded")
    
    tokens = tokenize(text)
    bigrams = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    
    # Create feature vector with same dimension as training
    vec = np.zeros(len(bigram_vocab))
    
    for bg in bigrams:
        if bg in bigram_vocab:
            vec[bigram_vocab[bg]] = 1
    
    return vec.reshape(1, -1)

# Load all models and vocabulary on startup
@app.on_event("startup")
async def startup_event():
    try:
        load_trained_model("n_gram_model.pkl")
        print("✓ N-gram model loaded")
    except Exception as e:
        print(f"✗ Failed to load N-gram model: {e}")
    
    try:
        load_naive_bayes_model("naive_bayes_model.pkl")
        print("✓ Naive Bayes model loaded")
    except Exception as e:
        print(f"✗ Failed to load Naive Bayes model: {e}")
    
    try:
        load_logistic_regression_model("lr_model.pkl")
        print("✓ Logistic Regression model loaded")
    except Exception as e:
        print(f"✗ Failed to load Logistic Regression model: {e}")
    
    try:
        load_bigram_vocab("bigram_vocab.pkl")
    except Exception as e:
        print(f"✗ Failed to load bigram vocabulary: {e}")

@app.get("/")
async def root():
    return {"message": "Multi-Model API is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "n_gram_vocab_size": len(lm.vocab),
        "naive_bayes_vocab_size": len(nb_model.vocab) if nb_model.is_loaded else 0,
        "logistic_regression_weights_shape": lr_model.W.shape if lr_model.is_loaded else "Not loaded",
        "bigram_vocab_size": len(bigram_vocab) if bigram_vocab else "Not loaded"
    }

@app.post("/predict-next", response_model=PredictionResponse)
async def predict_next_word(request: PredictionRequest):
    try:
        if request.model_type == "n_gram":
            # N-gram next word prediction
            tokens = request.sentence.strip().split()
            
            if not tokens:
                raise HTTPException(status_code=400, detail="Sentence cannot be empty")
            
            previous_word = tokens[-1].lower()
            predictions = lm.predict_next_word(previous_word, request.top_k)
            
            formatted_predictions = [
                WordPrediction(word=word, probability=prob) 
                for word, prob in predictions
            ]
            
            return PredictionResponse(
                model_used="n_gram",
                previous_word=previous_word,
                predictions=formatted_predictions
            )
            
        elif request.model_type == "naive_bayes":
            # Naive Bayes spam classification
            if not request.sentence.strip():
                raise HTTPException(status_code=400, detail="Text cannot be empty")
            
            prediction = nb_model.predict_single(request.sentence)
            
            return PredictionResponse(
                model_used="naive_bayes",
                spam_prediction=SpamPrediction(
                    classification=prediction["class"],
                    confidence=prediction["confidence"],
                    probabilities=prediction["probabilities"]
                )
            )
            
        elif request.model_type == "logistic_regression":
            # Logistic Regression spam classification
            if not request.sentence.strip():
                raise HTTPException(status_code=400, detail="Text cannot be empty")
            
            if bigram_vocab is None:
                raise HTTPException(status_code=500, detail="Bigram vocabulary not loaded")
            
            # Extract features and predict
            features = extract_features(request.sentence)
            
            # Check if feature dimension matches model expectations
            if lr_model.is_loaded and features.shape[1] != lr_model.W.shape[0]:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Feature dimension mismatch. Expected {lr_model.W.shape[0]}, got {features.shape[1]}"
                )
            
            prediction = lr_model.predict_single(features)
            
            return PredictionResponse(
                model_used="logistic_regression",
                spam_prediction=SpamPrediction(
                    classification=prediction["class"],
                    confidence=prediction["confidence"],
                    probabilities=prediction["probabilities"]
                )
            )
            
        else:
            raise HTTPException(status_code=400, detail="Invalid model type. Use 'n_gram', 'naive_bayes', or 'logistic_regression'")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)