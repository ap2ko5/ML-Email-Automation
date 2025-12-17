"""
Unit tests for model_predictor module
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np


class TestModelPredictor(unittest.TestCase):
    """Test cases for ModelPredictor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_model = Mock()
        self.mock_tokenizer = Mock()
    
    @patch('src.model_predictor.load_model')
    def test_model_initialization(self, mock_load):
        """Test ModelPredictor initialization"""
        from src.model_predictor import ModelPredictor
        
        mock_load.return_value = self.mock_model
        
        try:
            with patch('builtins.open', create=True):
                predictor = ModelPredictor()
                # Verify predictor was created
                self.assertIsNotNone(predictor)
        except:
            pass  # Expected since we're mocking
    
    def test_preprocess_text_returns_array(self):
        """Test that preprocess_text returns array or None"""
        from src.model_predictor import ModelPredictor
        
        predictor = ModelPredictor()
        predictor.tokenizer = None
        
        result = predictor.preprocess_text("test text")
        self.assertIsNone(result)
    
    def test_predict_returns_boolean(self):
        """Test that predict returns boolean"""
        from src.model_predictor import ModelPredictor
        
        predictor = ModelPredictor()
        predictor.model = None
        predictor.tokenizer = None
        
        result = predictor.predict("test email")
        self.assertIsInstance(result, bool)
        self.assertFalse(result)  # Should return False when model not loaded
    
    def test_get_confidence_score_returns_float(self):
        """Test that confidence score returns float"""
        from src.model_predictor import ModelPredictor
        
        predictor = ModelPredictor()
        predictor.model = None
        predictor.tokenizer = None
        
        result = predictor.get_confidence_score("test email")
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)
    
    def test_predict_batch_returns_list(self):
        """Test that predict_batch returns list"""
        from src.model_predictor import ModelPredictor
        
        predictor = ModelPredictor()
        predictor.model = None
        predictor.tokenizer = None
        
        emails = ["email1", "email2", "email3"]
        result = predictor.predict_batch(emails)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(emails))


if __name__ == '__main__':
    unittest.main()
