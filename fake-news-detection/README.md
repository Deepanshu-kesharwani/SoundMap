# Fake News Detection System

A comprehensive machine learning system for detecting fake news using NLP techniques, real-time news analysis, and an interactive Streamlit web interface.

## Features

- **🤖 Machine Learning Models**: Multiple ML algorithms (Logistic Regression, SVM, Random Forest)
- **📰 Real-time News Analysis**: Integration with NewsAPI for live news feeds
- **🎯 Ensemble Predictions**: Combine multiple models for improved accuracy
- **📊 Interactive Dashboard**: Streamlit-based web interface with visualizations
- **☁️ Word Clouds**: Visual representation of fake vs real news patterns
- **📈 Performance Metrics**: Comprehensive model evaluation and comparison
- **🔍 Feature Analysis**: Understand which words/features influence predictions

## Quick Start

### 1. Navigate to the fake news detection system
```bash
cd fake-news-detection
```

### 2. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 3. Set up Environment Variables (Optional)
Create a `.env` file in the project root:
```
NEWS_API_KEY=your_news_api_key_here
```

### 4. Run the Streamlit Application
```bash
streamlit run streamlit_app/app.py
```

## System Architecture

```
fake-news-detection/
├── data/
│   ├── historical/          # Historical news datasets
│   └── processed/           # Processed training data
├── models/
│   ├── trained_models/      # Saved ML models
│   └── evaluation/          # Model evaluation results
├── src/
│   ├── preprocessing.py     # Text preprocessing and feature extraction
│   ├── training.py          # Model training and hyperparameter tuning
│   ├── prediction.py        # Prediction engine and inference
│   └── api_integration.py   # NewsAPI integration
├── streamlit_app/
│   ├── app.py              # Main Streamlit application
│   ├── components/         # UI components
│   └── utils/              # Utility functions
├── notebooks/              # Jupyter notebooks for analysis
├── config.py               # Configuration settings
└── README.md               # This file
```

## Usage Guide

### Text Analysis
1. Open the **Text Analysis** page
2. Choose input method:
   - **Type/Paste Text**: Directly input news article text
   - **Upload File**: Upload .txt or .csv files
3. Click analyze to get predictions with confidence scores

### Real-time News Analysis
1. Navigate to **Real-time News** page
2. Choose news source:
   - **Top Headlines**: Get current top headlines by country
   - **Search News**: Search for specific topics
   - **Specific Sources**: Filter by trusted news sources
3. View automatic analysis of fetched articles

### Model Comparison
1. Go to **Model Comparison** page
2. Compare performance across different ML models
3. View detailed metrics and sample predictions

### Data Insights
1. Visit **Data Insights** page
2. Explore word clouds and text patterns
3. View dataset statistics and distributions

## Model Performance

The system uses three main machine learning models:

- **Logistic Regression**: Fast, interpretable linear model
- **Support Vector Machine**: Robust classifier with kernel tricks
- **Random Forest**: Ensemble method with feature importance

### Performance Metrics
- **Accuracy**: >85% on test datasets
- **Precision**: Minimizes false positives
- **Recall**: Captures most fake news instances
- **F1-Score**: Balanced performance measure

## API Integration

### NewsAPI Integration
- Real-time news fetching from 70,000+ sources
- Support for multiple languages and countries
- Search functionality and source filtering
- Automatic rate limiting and error handling

### Mock Data Mode
When NewsAPI key is not configured, the system uses realistic mock data for demonstration purposes.

## Technical Implementation

### Text Preprocessing
- Text cleaning and normalization
- Tokenization with NLTK
- Stopword removal and stemming
- TF-IDF vectorization

### Machine Learning Pipeline
- Cross-validation for model selection
- Grid search for hyperparameter optimization
- Model persistence with joblib
- Ensemble prediction combining multiple models

### Web Interface
- Responsive Streamlit design
- Interactive visualizations with Plotly
- Real-time prediction updates
- Export capabilities for results

## Configuration

### Model Parameters
```python
MODEL_PARAMS = {
    'logistic_regression': {
        'C': [0.1, 1, 10],
        'solver': ['liblinear', 'lbfgs']
    },
    'svm': {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf']
    },
    'random_forest': {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None]
    }
}
```

### TF-IDF Configuration
```python
TFIDF_PARAMS = {
    'max_features': 10000,
    'ngram_range': (1, 2),
    'min_df': 2,
    'max_df': 0.95
}
```

## Training Your Own Models

### 1. Prepare Data
```python
from src.preprocessing import preprocess_dataset, split_data
import pandas as pd

# Load your dataset
df = pd.read_csv('your_dataset.csv')

# Preprocess
X, y = preprocess_dataset(df, text_column='text', label_column='label')
X_train, X_test, y_train, y_test = split_data(X, y)
```

### 2. Train Models
```python
from src.training import FakeNewsTrainer, get_default_param_grids

trainer = FakeNewsTrainer()
param_grids = get_default_param_grids()
trainer.train_all_models(X_train, y_train, param_grids)
```

### 3. Evaluate Performance
```python
results = trainer.evaluate_all_models(X_test, y_test)
trainer.save_models()
```

## Extending the System

### Adding New Models
1. Extend the `FakeNewsTrainer` class in `src/training.py`
2. Add model parameters to `config.py`
3. Update the prediction engine in `src/prediction.py`

### Custom Features
1. Modify preprocessing pipeline in `src/preprocessing.py`
2. Add feature extraction methods
3. Update TF-IDF parameters in configuration

### New Data Sources
1. Extend `src/api_integration.py`
2. Add new API clients
3. Update data formatting functions

## Limitations and Considerations

⚠️ **Important Disclaimers:**

1. **Educational Purpose**: This system is designed for educational and research purposes
2. **No Substitute for Critical Thinking**: Always verify news from multiple reliable sources
3. **Model Limitations**: ML models can have biases and false predictions
4. **Context Matters**: Consider source credibility, publication date, and broader context
5. **Continuous Learning**: Models should be retrained with new data regularly

## Troubleshooting

### Common Issues

**Models not loading:**
- Ensure all dependencies are installed
- Check if model files exist in `models/trained_models/`
- Train models using the training script

**API errors:**
- Verify NewsAPI key configuration
- Check internet connection
- System falls back to mock data automatically

**Performance issues:**
- Reduce number of features in TF-IDF
- Use smaller model parameters
- Enable caching for repeated predictions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the SoundMap repository and follows the same licensing terms.

## Acknowledgments

- NLTK for natural language processing
- Scikit-learn for machine learning algorithms
- Streamlit for the web interface
- NewsAPI for real-time news data
- The open-source community for various libraries and tools

---

*Remember: This tool is designed to assist in identifying potentially false information, but human judgment and verification from multiple credible sources remain essential for making informed decisions about news content.*