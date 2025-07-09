"""
Data Preprocessing Module for Fake News Detection
Handles text cleaning, tokenization, TF-IDF vectorization, and data splitting
"""

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pickle
import os
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class TextPreprocessor:
    """Class for preprocessing text data for fake news detection"""
    
    def __init__(self, 
                 max_features: int = 10000,
                 ngram_range: Tuple[int, int] = (1, 2),
                 min_df: int = 2,
                 max_df: float = 0.95):
        """
        Initialize the text preprocessor
        
        Args:
            max_features: Maximum number of features for TF-IDF
            ngram_range: Range of n-grams to extract
            min_df: Minimum document frequency
            max_df: Maximum document frequency
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        self.vectorizer = None
        self.stemmer = PorterStemmer()
        
        # Initialize stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves'])
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text string
        """
        if pd.isna(text) or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def tokenize_and_stem(self, text: str) -> str:
        """
        Tokenize text and apply stemming
        
        Args:
            text: Cleaned text string
            
        Returns:
            Processed text string
        """
        try:
            # Tokenize
            tokens = word_tokenize(text)
            
            # Remove stopwords and apply stemming
            tokens = [self.stemmer.stem(token) for token in tokens 
                     if token not in self.stop_words and len(token) > 2]
            
            return ' '.join(tokens)
        except:
            # Fallback if NLTK tokenization fails
            words = text.split()
            words = [word for word in words if word not in self.stop_words and len(word) > 2]
            return ' '.join(words)
    
    def preprocess_text(self, text: str) -> str:
        """
        Complete text preprocessing pipeline
        
        Args:
            text: Raw text string
            
        Returns:
            Fully processed text string
        """
        text = self.clean_text(text)
        text = self.tokenize_and_stem(text)
        return text
    
    def fit_vectorizer(self, texts: list) -> None:
        """
        Fit TF-IDF vectorizer on training texts
        
        Args:
            texts: List of preprocessed text strings
        """
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            stop_words='english',
            ngram_range=self.ngram_range,
            min_df=self.min_df,
            max_df=self.max_df
        )
        self.vectorizer.fit(texts)
    
    def transform_texts(self, texts: list) -> np.ndarray:
        """
        Transform texts using fitted vectorizer
        
        Args:
            texts: List of preprocessed text strings
            
        Returns:
            TF-IDF feature matrix
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit_vectorizer first.")
        
        return self.vectorizer.transform(texts).toarray()
    
    def save_vectorizer(self, filepath: str) -> None:
        """Save fitted vectorizer to file"""
        if self.vectorizer is None:
            raise ValueError("No vectorizer to save")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_vectorizer(self, filepath: str) -> None:
        """Load vectorizer from file"""
        with open(filepath, 'rb') as f:
            self.vectorizer = pickle.load(f)

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load dataset from file
    
    Args:
        filepath: Path to dataset file
        
    Returns:
        DataFrame with news data
    """
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format")
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def prepare_sample_data() -> pd.DataFrame:
    """
    Create sample data for demonstration
    
    Returns:
        DataFrame with sample news data
    """
    sample_data = {
        'title': [
            'Scientists Discover New Species in Amazon Rainforest',
            'BREAKING: Aliens Found Living Among Us, Government Confirms',
            'Stock Market Reaches New High Amid Economic Recovery',
            'Local Man Claims He Can Talk to Animals, Experts Skeptical',
            'New Study Shows Benefits of Regular Exercise',
            'SHOCKING: Water Found to be Wet, Scientists Stunned',
            'Climate Change Impact on Arctic Ice Documented',
            'Miracle Cure Discovered by Grandmother in Kitchen',
        ],
        'text': [
            'Researchers from leading universities have documented a new species of bird in the Amazon rainforest, highlighting the importance of conservation efforts.',
            'Government officials today confirmed that aliens have been living among humans for decades. The beings reportedly work in various industries.',
            'The stock market closed at record highs today as investors showed confidence in the economic recovery following recent policy changes.',
            'A local resident claims he has developed the ability to communicate with animals after a hiking accident. Veterinarians remain skeptical.',
            'A comprehensive study involving 10,000 participants over 5 years confirms that regular exercise significantly improves mental and physical health.',
            'In a groundbreaking study, scientists have confirmed that water has the property of being wet. This discovery challenges previous assumptions.',
            'New satellite data reveals accelerated melting of Arctic ice, providing concrete evidence of climate change impacts on polar regions.',
            'A grandmother claims her homemade soup can cure any illness. Medical experts urge caution and proper medical consultation for health issues.',
        ],
        'label': [1, 0, 1, 0, 1, 0, 1, 0]  # 1 = real, 0 = fake
    }
    
    return pd.DataFrame(sample_data)

def split_data(X: np.ndarray, y: np.ndarray, 
               test_size: float = 0.2, 
               random_state: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split data into training and testing sets
    
    Args:
        X: Feature matrix
        y: Target labels
        test_size: Proportion of data for testing
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def preprocess_dataset(df: pd.DataFrame, 
                      text_column: str = 'text',
                      label_column: str = 'label',
                      title_column: Optional[str] = 'title') -> Tuple[np.ndarray, np.ndarray]:
    """
    Complete preprocessing pipeline for a dataset
    
    Args:
        df: DataFrame with news data
        text_column: Name of text content column
        label_column: Name of label column
        title_column: Name of title column (optional)
        
    Returns:
        Tuple of (features, labels)
    """
    # Initialize preprocessor
    preprocessor = TextPreprocessor()
    
    # Combine title and text if title column exists
    if title_column and title_column in df.columns:
        combined_text = df[title_column].fillna('') + ' ' + df[text_column].fillna('')
    else:
        combined_text = df[text_column].fillna('')
    
    # Preprocess texts
    processed_texts = [preprocessor.preprocess_text(text) for text in combined_text]
    
    # Fit vectorizer and transform texts
    preprocessor.fit_vectorizer(processed_texts)
    features = preprocessor.transform_texts(processed_texts)
    
    # Get labels
    labels = df[label_column].values
    
    # Save vectorizer
    os.makedirs('models/trained_models', exist_ok=True)
    preprocessor.save_vectorizer('models/trained_models/vectorizer.pkl')
    
    return features, labels

if __name__ == "__main__":
    # Demo preprocessing with sample data
    print("Creating sample data...")
    df = prepare_sample_data()
    print(f"Sample data shape: {df.shape}")
    print("\nSample titles:")
    print(df['title'].head())
    
    print("\nPreprocessing data...")
    X, y = preprocess_dataset(df)
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Training set: {X_train.shape}, {y_train.shape}")
    print(f"Test set: {X_test.shape}, {y_test.shape}")
    
    print("\nPreprocessing completed successfully!")