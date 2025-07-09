"""
Prediction Engine for Fake News Detection
Handles model loading, inference, and batch predictions
"""

import pandas as pd
import numpy as np
import pickle
import os
from typing import Dict, List, Tuple, Union
import warnings
warnings.filterwarnings('ignore')

from preprocessing import TextPreprocessor

class FakeNewsPredictor:
    """Class for making predictions with trained fake news detection models"""
    
    def __init__(self, models_directory: str = 'models/trained_models'):
        """
        Initialize the predictor
        
        Args:
            models_directory: Directory containing trained models
        """
        self.models_directory = models_directory
        self.models = {}
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        
        # Load models and vectorizer
        self._load_models()
        self._load_vectorizer()
    
    def _load_models(self) -> None:
        """Load all available trained models"""
        model_files = {
            'logistic_regression': 'logistic_regression.pkl',
            'svm': 'svm.pkl',
            'random_forest': 'random_forest.pkl'
        }
        
        for model_name, filename in model_files.items():
            filepath = os.path.join(self.models_directory, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'rb') as f:
                        self.models[model_name] = pickle.load(f)
                    print(f"Loaded {model_name} model")
                except Exception as e:
                    print(f"Error loading {model_name}: {e}")
            else:
                print(f"Model file not found: {filepath}")
    
    def _load_vectorizer(self) -> None:
        """Load the TF-IDF vectorizer"""
        vectorizer_path = os.path.join(self.models_directory, 'vectorizer.pkl')
        if os.path.exists(vectorizer_path):
            try:
                self.preprocessor.load_vectorizer(vectorizer_path)
                print("Loaded TF-IDF vectorizer")
            except Exception as e:
                print(f"Error loading vectorizer: {e}")
        else:
            print(f"Vectorizer file not found: {vectorizer_path}")
    
    def preprocess_text(self, text: str) -> np.ndarray:
        """
        Preprocess a single text for prediction
        
        Args:
            text: Raw text string
            
        Returns:
            Preprocessed feature vector
        """
        if self.preprocessor.vectorizer is None:
            raise ValueError("Vectorizer not loaded. Cannot preprocess text.")
        
        # Clean and preprocess text
        processed_text = self.preprocessor.preprocess_text(text)
        
        # Transform to feature vector
        features = self.preprocessor.transform_texts([processed_text])
        
        return features
    
    def predict_single(self, 
                      text: str, 
                      model_name: str = 'random_forest') -> Dict[str, Union[int, float, str]]:
        """
        Make prediction for a single text
        
        Args:
            text: Text to classify
            model_name: Name of the model to use
            
        Returns:
            Dictionary with prediction results
        """
        if model_name not in self.models:
            available_models = list(self.models.keys())
            if not available_models:
                raise ValueError("No models available for prediction")
            model_name = available_models[0]
            print(f"Model '{model_name}' not available. Using '{model_name}'")
        
        # Preprocess text
        features = self.preprocess_text(text)
        
        # Make prediction
        model = self.models[model_name]
        prediction = model.predict(features)[0]
        
        # Get prediction probability if available
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities)
            fake_prob = probabilities[0]
            real_prob = probabilities[1]
        else:
            confidence = 0.5
            fake_prob = 0.5
            real_prob = 0.5
        
        # Interpret prediction
        label = "Real" if prediction == 1 else "Fake"
        
        return {
            'prediction': int(prediction),
            'label': label,
            'confidence': float(confidence),
            'fake_probability': float(fake_prob),
            'real_probability': float(real_prob),
            'model_used': model_name
        }
    
    def predict_batch(self, 
                     texts: List[str], 
                     model_name: str = 'random_forest') -> List[Dict[str, Union[int, float, str]]]:\n        \"\"\"\n        Make predictions for multiple texts\n        \n        Args:\n            texts: List of texts to classify\n            model_name: Name of the model to use\n            \n        Returns:\n            List of prediction dictionaries\n        \"\"\"\n        results = []\n        \n        for text in texts:\n            try:\n                result = self.predict_single(text, model_name)\n                results.append(result)\n            except Exception as e:\n                results.append({\n                    'prediction': 0,\n                    'label': 'Error',\n                    'confidence': 0.0,\n                    'fake_probability': 0.0,\n                    'real_probability': 0.0,\n                    'model_used': model_name,\n                    'error': str(e)\n                })\n        \n        return results\n    \n    def predict_with_all_models(self, text: str) -> Dict[str, Dict[str, Union[int, float, str]]]:\n        \"\"\"\n        Make predictions using all available models\n        \n        Args:\n            text: Text to classify\n            \n        Returns:\n            Dictionary with results from all models\n        \"\"\"\n        results = {}\n        \n        for model_name in self.models.keys():\n            try:\n                results[model_name] = self.predict_single(text, model_name)\n            except Exception as e:\n                results[model_name] = {\n                    'prediction': 0,\n                    'label': 'Error',\n                    'confidence': 0.0,\n                    'fake_probability': 0.0,\n                    'real_probability': 0.0,\n                    'model_used': model_name,\n                    'error': str(e)\n                }\n        \n        return results\n    \n    def get_ensemble_prediction(self, text: str) -> Dict[str, Union[int, float, str]]:\n        \"\"\"\n        Get ensemble prediction by averaging all model predictions\n        \n        Args:\n            text: Text to classify\n            \n        Returns:\n            Dictionary with ensemble prediction\n        \"\"\"\n        all_predictions = self.predict_with_all_models(text)\n        \n        if not all_predictions:\n            raise ValueError(\"No models available for ensemble prediction\")\n        \n        # Calculate ensemble averages\n        valid_predictions = [p for p in all_predictions.values() if 'error' not in p]\n        \n        if not valid_predictions:\n            raise ValueError(\"All models failed to make predictions\")\n        \n        avg_fake_prob = np.mean([p['fake_probability'] for p in valid_predictions])\n        avg_real_prob = np.mean([p['real_probability'] for p in valid_predictions])\n        avg_confidence = np.mean([p['confidence'] for p in valid_predictions])\n        \n        # Ensemble prediction\n        ensemble_prediction = 1 if avg_real_prob > avg_fake_prob else 0\n        ensemble_label = \"Real\" if ensemble_prediction == 1 else \"Fake\"\n        \n        return {\n            'prediction': int(ensemble_prediction),\n            'label': ensemble_label,\n            'confidence': float(avg_confidence),\n            'fake_probability': float(avg_fake_prob),\n            'real_probability': float(avg_real_prob),\n            'model_used': 'ensemble',\n            'individual_predictions': all_predictions,\n            'models_used': len(valid_predictions)\n        }\n    \n    def analyze_text_features(self, text: str, top_n: int = 10) -> Dict[str, List[Tuple[str, float]]]:\n        \"\"\"\n        Analyze which features (words/n-grams) are most important for prediction\n        \n        Args:\n            text: Text to analyze\n            top_n: Number of top features to return\n            \n        Returns:\n            Dictionary with top positive and negative features\n        \"\"\"\n        if self.preprocessor.vectorizer is None:\n            raise ValueError(\"Vectorizer not loaded\")\n        \n        # Preprocess and get features\n        features = self.preprocess_text(text)\n        feature_names = self.preprocessor.vectorizer.get_feature_names_out()\n        \n        # Get feature scores from a linear model if available\n        if 'logistic_regression' in self.models:\n            model = self.models['logistic_regression']\n            if hasattr(model, 'coef_'):\n                feature_scores = features * model.coef_[0]\n                feature_importance = list(zip(feature_names, feature_scores[0]))\n                \n                # Sort by importance\n                feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)\n                \n                # Separate positive and negative features\n                positive_features = [(name, score) for name, score in feature_importance if score > 0][:top_n]\n                negative_features = [(name, score) for name, score in feature_importance if score < 0][:top_n]\n                \n                return {\n                    'positive_features': positive_features,  # Support \"Real\" prediction\n                    'negative_features': negative_features,  # Support \"Fake\" prediction\n                    'top_features': feature_importance[:top_n]\n                }\n        \n        # Fallback: return top TF-IDF features\n        feature_scores = features[0]\n        feature_importance = list(zip(feature_names, feature_scores))\n        feature_importance.sort(key=lambda x: x[1], reverse=True)\n        \n        return {\n            'top_features': feature_importance[:top_n],\n            'positive_features': feature_importance[:top_n//2],\n            'negative_features': feature_importance[top_n//2:top_n]\n        }\n    \n    def get_model_info(self) -> Dict[str, Dict[str, str]]:\n        \"\"\"\n        Get information about loaded models\n        \n        Returns:\n            Dictionary with model information\n        \"\"\"\n        model_info = {}\n        \n        for model_name, model in self.models.items():\n            model_info[model_name] = {\n                'type': type(model).__name__,\n                'parameters': str(model.get_params()),\n                'available': True\n            }\n        \n        return model_info\n    \n    def is_ready(self) -> bool:\n        \"\"\"\n        Check if predictor is ready to make predictions\n        \n        Returns:\n            True if models and vectorizer are loaded\n        \"\"\"\n        return len(self.models) > 0 and self.preprocessor.vectorizer is not None\n\ndef create_fallback_predictor() -> FakeNewsPredictor:\n    \"\"\"\n    Create a fallback predictor with a simple rule-based approach\n    when trained models are not available\n    \n    Returns:\n        Simple predictor instance\n    \"\"\"\n    class SimpleFakeNewsPredictor:\n        def __init__(self):\n            # Simple keywords that might indicate fake news\n            self.fake_indicators = [\n                'shocking', 'unbelievable', 'miracle', 'secret', 'they dont want you to know',\n                'doctors hate', 'amazing discovery', 'this one trick', 'breaking news',\n                'urgent', 'must read', 'viral', 'exposed', 'revealed'\n            ]\n        \n        def predict_single(self, text: str, model_name: str = 'simple_rule') -> Dict[str, Union[int, float, str]]:\n            text_lower = text.lower()\n            fake_score = sum(1 for keyword in self.fake_indicators if keyword in text_lower)\n            \n            # Simple heuristic: if many fake indicators, likely fake\n            is_fake = fake_score >= 2\n            confidence = min(0.6 + fake_score * 0.1, 0.9) if is_fake else 0.6\n            \n            prediction = 0 if is_fake else 1\n            label = \"Fake\" if is_fake else \"Real\"\n            \n            return {\n                'prediction': prediction,\n                'label': label,\n                'confidence': confidence,\n                'fake_probability': 1 - confidence if not is_fake else confidence,\n                'real_probability': confidence if not is_fake else 1 - confidence,\n                'model_used': 'simple_rule_based',\n                'fake_indicators_found': fake_score\n            }\n        \n        def is_ready(self) -> bool:\n            return True\n    \n    return SimpleFakeNewsPredictor()\n\nif __name__ == \"__main__\":\n    # Demo prediction\n    print(\"Initializing predictor...\")\n    \n    try:\n        predictor = FakeNewsPredictor()\n        \n        if not predictor.is_ready():\n            print(\"Trained models not available. Using fallback predictor.\")\n            predictor = create_fallback_predictor()\n        \n        # Test predictions\n        test_texts = [\n            \"Scientists at MIT have developed a new renewable energy technology that could revolutionize the industry.\",\n            \"SHOCKING: This miracle cure will heal any disease! Doctors don't want you to know this secret!\",\n            \"The stock market experienced volatility today due to economic uncertainty.\",\n            \"BREAKING: Aliens found living in underground cities! Government cover-up exposed!\"\n        ]\n        \n        print(\"\\nMaking predictions...\")\n        for i, text in enumerate(test_texts, 1):\n            result = predictor.predict_single(text)\n            print(f\"\\nText {i}: {text[:60]}...\")\n            print(f\"Prediction: {result['label']} (confidence: {result['confidence']:.2f})\")\n            \n    except Exception as e:\n        print(f\"Error in prediction demo: {e}\")\n        print(\"Using fallback predictor...\")\n        predictor = create_fallback_predictor()\n        \n        result = predictor.predict_single(\"This is a test article about current events.\")\n        print(f\"Fallback prediction: {result}\")