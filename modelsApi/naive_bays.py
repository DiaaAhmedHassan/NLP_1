import pickle
import numpy as np
from collections import Counter
import re

def tokenize(text):
    """Simple tokenization function - same as used during training"""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

class NaiveBayesTextClassifier:
    def __init__(self):
        self.class_priors = {}     # Stores prior probabilities for each class (P(class))
        self.word_counts = {}      # Stores word counts per class
        self.vocab = set()         # Stores all unique words
        self.class_totals = {}     # Stores total number of words per class
        self.is_loaded = False

    def load_model(self, model_path):
        """Load trained model from pickle file"""
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        
        self.class_priors = model_data["class_priors"]
        self.word_counts = model_data["word_counts"]
        self.vocab = model_data["vocab"]
        self.class_totals = model_data["class_totals"]
        self.is_loaded = True
        print(f"Naive Bayes model loaded. Vocabulary size: {len(self.vocab)}")

    def predict_single(self, text):
        """Predict class for a single text input"""
        if not self.is_loaded:
            raise ValueError("Model not loaded")
            
        tokens = tokenize(text)
        vocab_size = len(self.vocab)
        log_probs = {}

        for c in [0, 1]:  # 0=Ham, 1=Spam
            log_prob = np.log(self.class_priors[c])

            # Calculate likelihood with Laplace smoothing
            for t in tokens:
                count = self.word_counts[c].get(t, 0)
                log_prob += np.log((count + 1) / (self.class_totals[c] + vocab_size))

            log_probs[c] = log_prob

        # Return the class with highest probability
        predicted_class = max(log_probs, key=log_probs.get)
        confidence = np.exp(log_probs[predicted_class])
        
        return {
            "class": "Ham" if predicted_class == 0 else "Spam",
            "confidence": float(confidence),
            "probabilities": {
                "Ham": float(np.exp(log_probs[0])),
                "Spam": float(np.exp(log_probs[1]))
            }
        }

    def predict_next_word(self, previous_word, top_k=5):
        """Dummy method to maintain same interface as n_gram model"""
        # For Naive Bayes, this doesn't make sense, so return empty
        return []

# Global model instance
nb_model = NaiveBayesTextClassifier()

def load_naive_bayes_model(model_path="naive_bayes_model.pkl"):
    """Load the trained Naive Bayes model"""
    nb_model.load_model(model_path)