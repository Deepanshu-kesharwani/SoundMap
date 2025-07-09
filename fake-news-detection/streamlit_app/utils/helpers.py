"""
Utility components for the Streamlit app
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any

def create_confidence_gauge(confidence: float, title: str = "Confidence") -> go.Figure:
    """
    Create a confidence gauge chart
    
    Args:
        confidence: Confidence value (0-1)
        title: Gauge title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 70], 'color': "yellow"},
                {'range': [70, 90], 'color': "orange"},
                {'range': [90, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=20))
    return fig

def create_prediction_bar_chart(predictions: Dict[str, Dict]) -> go.Figure:
    """
    Create a bar chart comparing model predictions
    
    Args:
        predictions: Dictionary of model predictions
        
    Returns:
        Plotly figure
    """
    models = []
    confidences = []
    labels = []
    
    for model_name, pred in predictions.items():
        if 'error' not in pred:
            models.append(model_name.replace('_', ' ').title())
            confidences.append(pred['confidence'])
            labels.append(pred['label'])
    
    fig = px.bar(
        x=models,
        y=confidences,
        color=labels,
        title="Model Prediction Comparison",
        labels={'x': 'Model', 'y': 'Confidence', 'color': 'Prediction'},
        color_discrete_map={'Real': 'green', 'Fake': 'red'}
    )
    
    fig.update_layout(height=400)
    return fig

def display_news_article_card(article: Dict, prediction: Dict) -> None:
    """
    Display a news article with prediction results
    
    Args:
        article: Article data
        prediction: Prediction results
    """
    # Article header
    st.markdown(f"### {article['title']}")
    
    # Article metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Source:** {article['source']}")
    with col2:
        st.write(f"**Author:** {article['author']}")
    with col3:
        st.write(f"**Published:** {article['published_at']}")
    
    # Article content
    st.write(f"**Description:** {article['description']}")
    
    # Prediction results
    if prediction['label'] == 'Fake':
        st.error(f"🚨 **Prediction: FAKE NEWS** (Confidence: {prediction['confidence']:.1%})")
    else:
        st.success(f"✅ **Prediction: REAL NEWS** (Confidence: {prediction['confidence']:.1%})")
    
    # Probability breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fake Probability", f"{prediction['fake_probability']:.1%}")
    with col2:
        st.metric("Real Probability", f"{prediction['real_probability']:.1%}")
    
    # Link to full article
    if article['url']:
        st.markdown(f"[Read full article]({article['url']})")

def create_performance_comparison_chart(performance_data: Dict) -> go.Figure:
    """
    Create a performance comparison chart for multiple models
    
    Args:
        performance_data: Dictionary with model performance metrics
        
    Returns:
        Plotly figure
    """
    df = pd.DataFrame(performance_data)
    
    fig = go.Figure()
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    colors = ['blue', 'red', 'green', 'orange']
    
    for i, metric in enumerate(metrics):
        if metric in df.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=df['Model'],
                y=df[metric],
                marker_color=colors[i]
            ))
    
    fig.update_layout(
        title='Model Performance Comparison',
        xaxis_title='Model',
        yaxis_title='Score',
        barmode='group',
        height=400
    )
    
    return fig

def display_text_statistics(text: str) -> None:
    """
    Display text statistics in a formatted way
    
    Args:
        text: Text to analyze
    """
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?')
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Word Count",
            value=len(words),
            help="Total number of words in the text"
        )
    
    with col2:
        st.metric(
            label="Character Count",
            value=len(text),
            help="Total number of characters including spaces"
        )
    
    with col3:
        st.metric(
            label="Sentences",
            value=sentences,
            help="Estimated number of sentences"
        )
    
    with col4:
        st.metric(
            label="Avg Word Length",
            value=f"{avg_word_length:.1f}",
            help="Average length of words in characters"
        )

def create_word_frequency_chart(text: str, top_n: int = 10) -> go.Figure:
    """
    Create a word frequency chart
    
    Args:
        text: Text to analyze
        top_n: Number of top words to show
        
    Returns:
        Plotly figure
    """
    import re
    from collections import Counter
    
    # Simple text processing
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count frequencies
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(top_n)
    
    if not top_words:
        # Return empty figure if no words found
        fig = go.Figure()
        fig.update_layout(title="No words found for frequency analysis")
        return fig
    
    words, counts = zip(*top_words)
    
    fig = px.bar(
        x=list(counts),
        y=list(words),
        orientation='h',
        title=f'Top {top_n} Most Frequent Words',
        labels={'x': 'Frequency', 'y': 'Words'}
    )
    
    fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
    return fig

def display_model_info(model_info: Dict) -> None:
    """
    Display information about loaded models
    
    Args:
        model_info: Dictionary with model information
    """
    st.markdown("### 🤖 Loaded Models")
    
    for model_name, info in model_info.items():
        with st.expander(f"{model_name.replace('_', ' ').title()}"):
            st.write(f"**Type:** {info['type']}")
            st.write(f"**Status:** {'✅ Available' if info['available'] else '❌ Not available'}")
            if 'parameters' in info:
                st.write(f"**Parameters:** {info['parameters'][:200]}...")

def create_confusion_matrix_heatmap(confusion_matrix: List[List[int]]) -> go.Figure:
    """
    Create a confusion matrix heatmap
    
    Args:
        confusion_matrix: 2x2 confusion matrix
        
    Returns:
        Plotly figure
    """
    import numpy as np
    
    cm = np.array(confusion_matrix)
    
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Fake', 'Predicted Real'],
        y=['Actual Fake', 'Actual Real'],
        hoverongaps=False,
        colorscale='Blues',
        showscale=True
    ))
    
    # Add text annotations
    for i in range(len(cm)):
        for j in range(len(cm[0])):
            fig.add_annotation(
                x=j, y=i,
                text=str(cm[i][j]),
                showarrow=False,
                font=dict(color="white" if cm[i][j] > cm.max()/2 else "black", size=16)
            )
    
    fig.update_layout(
        title='Confusion Matrix',
        xaxis_title='Predicted',
        yaxis_title='Actual',
        height=400
    )
    
    return fig

def format_percentage(value: float) -> str:
    """
    Format a float as a percentage string
    
    Args:
        value: Float value (0-1)
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.1%}"

def safe_get_dict_value(dictionary: Dict, key: str, default: Any = "N/A") -> Any:
    """
    Safely get a value from a dictionary
    
    Args:
        dictionary: Dictionary to search
        key: Key to look for
        default: Default value if key not found
        
    Returns:
        Value from dictionary or default
    """
    return dictionary.get(key, default)