"""
Configuration file for the Fake News Detection System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_news_api_key_here")
NEWS_API_BASE_URL = "https://newsapi.org/v2"

# Model Configuration
MODEL_PARAMS = {
    'logistic_regression': {
        'C': [0.1, 1, 10],
        'solver': ['liblinear', 'lbfgs'],
        'max_iter': [1000]
    },
    'svm': {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'],
        'gamma': ['scale', 'auto']
    },
    'random_forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5]
    }
}

# Data Configuration
DATA_PATHS = {
    'historical': 'data/historical/',
    'processed': 'data/processed/',
    'models': 'models/trained_models/',
    'evaluation': 'models/evaluation/'
}

# TF-IDF Configuration
TFIDF_PARAMS = {
    'max_features': 10000,
    'stop_words': 'english',
    'ngram_range': (1, 2),
    'min_df': 2,
    'max_df': 0.95
}

# Training Configuration
TRAIN_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'cv_folds': 5,
    'scoring': 'accuracy'
}

# UI Configuration
UI_CONFIG = {
    'page_title': "Fake News Detection System",
    'page_icon': "📰",
    'layout': "wide",
    'confidence_threshold': 0.7
}

# File paths
SAMPLE_DATA_URL = "https://raw.githubusercontent.com/datasets/fake-news/master/data/news.csv"