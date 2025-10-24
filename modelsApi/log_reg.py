import pickle
import numpy as np

class LogisticRegressionScratch:
    def __init__(self, lr=0.1, epochs=20):
        self.lr = lr
        self.epochs = epochs
        self.W = None
        self.b = 0
        self.is_loaded = False
    
    def load_model(self, model_path):
        """Load trained model from pickle file - SAME PATTERN AS OTHERS"""
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        
        self.W = model_data["W"]
        self.b = model_data["b"]
        self.lr = model_data.get("lr", 0.1)
        self.epochs = model_data.get("epochs", 10)
        self.is_loaded = True
        print(f"Logistic Regression model loaded. Weight shape: {self.W.shape}")
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def predict_proba(self, X):
        """Predict probabilities for a single sample or multiple samples"""
        if not self.is_loaded:
            raise ValueError("Model not loaded")
        
        # Ensure X is 2D array
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Calculate probabilities
        linear_output = np.dot(X, self.W) + self.b
        probabilities = self.sigmoid(linear_output)
        return probabilities
    
    def predict_single(self, features):
        """Predict class for a single feature vector"""
        if not self.is_loaded:
            raise ValueError("Model not loaded")
        
        probability = self.predict_proba(features)[0]
        predicted_class = 1 if probability >= 0.5 else 0
        
        return {
            "class": "Spam" if predicted_class == 1 else "Ham",
            "confidence": float(probability if predicted_class == 1 else 1 - probability),
            "probability": float(probability),
            "probabilities": {
                "Ham": float(1 - probability),
                "Spam": float(probability)
            }
        }

# Global model instance - SAME PATTERN AS OTHERS
lr_model = LogisticRegressionScratch()

def load_logistic_regression_model(model_path="lr_model.pkl"):
    """Load the trained Logistic Regression model - SAME PATTERN AS OTHERS"""
    lr_model.load_model(model_path)
    print(f"Logistic Regression model loaded successfully. Weight shape: {lr_model.W.shape}")