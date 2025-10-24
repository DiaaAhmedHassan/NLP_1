import pickle
from collections import defaultdict, Counter

class BigramLanguageModel:
    def __init__(self):
        self.bigram_counts = defaultdict(Counter)
        self.unigram_counts = Counter()
        self.vocab = set()
    
    def load_model(self, model_path):
        """Load trained model from pickle file"""
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        
        self.bigram_counts = model_data["bigram_counts"]
        self.unigram_counts = model_data["unigram_counts"]
        self.vocab = model_data["vocab"]
    
    def prob(self, w_prev, w_next):
        """Calculate probability with Laplace smoothing"""
        vocab_size = len(self.vocab)
        count_prev = self.unigram_counts.get(w_prev, 0)
        count_bigram = self.bigram_counts.get(w_prev, Counter()).get(w_next, 0)
        return (count_bigram + 1) / (count_prev + vocab_size)
    
    def predict_next_word(self, previous_word, top_k=5):
        """Predict the most likely next words given a previous word"""
        if previous_word not in self.bigram_counts:
            return []
        
        # Get all possible next words and their probabilities
        next_words = self.bigram_counts[previous_word]
        word_probs = []
        
        for word in next_words:
            probability = self.prob(previous_word, word)
            word_probs.append((word, probability))
        
        # Sort by probability (descending) and return top k
        word_probs.sort(key=lambda x: x[1], reverse=True)
        return word_probs[:top_k]

# Global model instance
lm = BigramLanguageModel()

def load_trained_model(model_path="n_gram_model.pkl"):
    """Load the trained model at startup"""
    lm.load_model(model_path)
    print(f"Model loaded successfully. Vocabulary size: {len(lm.vocab)}")