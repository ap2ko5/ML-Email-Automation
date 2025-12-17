"""
Model Predictor Module

Handles LSTM model loading and prediction.
"""

import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class ModelPredictor:
    """Load and use LSTM model for predictions"""

    def __init__(self, model_path='models/lstm_model.h5', tokenizer_path='models/tokenizer.pickle'):
        """Initialize model predictor
        
        Args:
            model_path: Path to saved LSTM model
            tokenizer_path: Path to saved tokenizer
        """
        try:
            self.model = load_model(model_path)
            with open(tokenizer_path, 'rb') as f:
                self.tokenizer = pickle.load(f)
            self.max_length = 100
        except Exception as e:
            print(f'Error loading model: {e}')
            self.model = None
            self.tokenizer = None

    def preprocess_text(self, text):
        """Preprocess email text
        
        Args:
            text: Raw email text
            
        Returns:
            Preprocessed sequence
        """
        if not self.tokenizer:
            return None
            
        # Convert to lowercase and remove special characters
        text = text.lower()
        
        # Tokenize
        sequences = self.tokenizer.texts_to_sequences([text])
        padded = pad_sequences(sequences, maxlen=self.max_length, padding='post')
        
        return padded

    def predict(self, email_text):
        """Predict if email is legitimate giveaway
        
        Args:
            email_text: Email subject and body
            
        Returns:
            True if legitimate, False otherwise
        """
        if not self.model or not self.tokenizer:
            print('Model not loaded')
            return False
            
        try:
            processed = self.preprocess_text(email_text)
            if processed is None:
                return False
                
            prediction = self.model.predict(processed, verbose=0)
            return prediction[0][0] > 0.5
            
        except Exception as e:
            print(f'Prediction error: {e}')
            return False

    def get_confidence_score(self, email_text):
        """Get confidence score for prediction
        
        Args:
            email_text: Email text
            
        Returns:
            Confidence score (0-1)
        """
        if not self.model or not self.tokenizer:
            return 0.0
            
        try:
            processed = self.preprocess_text(email_text)
            if processed is None:
                return 0.0
                
            prediction = self.model.predict(processed, verbose=0)
            return float(prediction[0][0])
            
        except Exception as e:
            print(f'Confidence score error: {e}')
            return 0.0

    def predict_batch(self, email_list):
        """Predict batch of emails
        
        Args:
            email_list: List of email texts
            
        Returns:
            List of predictions
        """
        return [self.predict(email) for email in email_list]
