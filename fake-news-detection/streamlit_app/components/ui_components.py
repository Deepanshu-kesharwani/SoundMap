"""
Streamlit components for the fake news detection app
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional

class PredictionDisplay:
    """Component for displaying prediction results"""
    
    @staticmethod
    def show_single_prediction(result: Dict[str, Any], show_details: bool = True) -> None:
        """
        Display a single prediction result
        
        Args:
            result: Prediction result dictionary
            show_details: Whether to show detailed information
        """
        # Main prediction result
        if result['label'] == 'Fake':
            st.error(f"🚨 **FAKE NEWS DETECTED**")
            st.markdown(f"**Confidence:** {result['confidence']:.1%}")
        else:
            st.success(f"✅ **REAL NEWS**")
            st.markdown(f"**Confidence:** {result['confidence']:.1%}")
        
        if show_details:
            # Probability breakdown
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Fake Probability", f"{result['fake_probability']:.1%}")
            with col2:
                st.metric("Real Probability", f"{result['real_probability']:.1%}")
            
            # Model used
            st.caption(f"Model used: {result.get('model_used', 'Unknown')}")
    
    @staticmethod
    def show_ensemble_prediction(result: Dict[str, Any]) -> None:
        """
        Display ensemble prediction results
        
        Args:
            result: Ensemble prediction result
        """
        st.markdown("### 🎯 Ensemble Prediction")
        
        # Main result
        if result['label'] == 'Fake':
            st.error(f"🚨 **ENSEMBLE PREDICTION: FAKE NEWS**")
        else:
            st.success(f"✅ **ENSEMBLE PREDICTION: REAL NEWS**")
        
        # Details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Confidence", f"{result['confidence']:.1%}")
        with col2:
            st.metric("Models Used", result.get('models_used', 0))
        with col3:
            fake_prob = result.get('fake_probability', 0)
            st.metric("Fake Probability", f"{fake_prob:.1%}")

class NewsDisplay:
    """Component for displaying news articles"""
    
    @staticmethod
    def show_article_summary(article: Dict[str, Any], prediction: Optional[Dict] = None) -> None:
        """
        Display a summary of a news article with optional prediction
        
        Args:
            article: Article data
            prediction: Optional prediction results
        """
        # Article title and basic info
        st.markdown(f"**{article.get('title', 'No title')}**")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.caption(f"Source: {article.get('source', 'Unknown')}")
            st.caption(f"Author: {article.get('author', 'Unknown')}")
            if article.get('published_at'):
                st.caption(f"Published: {article['published_at']}")
            
            # Description
            if article.get('description'):
                st.write(article['description'])
        
        with col2:
            if prediction:
                if prediction['label'] == 'Fake':
                    st.error(f"FAKE ({prediction['confidence']:.0%})")
                else:
                    st.success(f"REAL ({prediction['confidence']:.0%})")
        
        # Link to full article
        if article.get('url'):
            st.markdown(f"[Read full article]({article['url']})")
    
    @staticmethod
    def show_article_grid(articles: List[Dict], predictions: List[Dict] = None) -> None:
        """
        Display articles in a grid layout
        
        Args:
            articles: List of article data
            predictions: Optional list of predictions
        """
        if not articles:
            st.info("No articles to display")
            return
        
        # Create grid layout
        cols = st.columns(2)
        
        for i, article in enumerate(articles):
            with cols[i % 2]:
                with st.container():
                    prediction = predictions[i] if predictions and i < len(predictions) else None
                    NewsDisplay.show_article_summary(article, prediction)
                    st.markdown("---")

class MetricsDisplay:
    """Component for displaying metrics and statistics"""
    
    @staticmethod
    def show_model_performance(metrics: Dict[str, float]) -> None:
        """
        Display model performance metrics
        
        Args:
            metrics: Dictionary of performance metrics
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            accuracy = metrics.get('accuracy', 0)
            st.metric("Accuracy", f"{accuracy:.1%}")
        
        with col2:
            precision = metrics.get('precision', 0)
            st.metric("Precision", f"{precision:.1%}")
        
        with col3:
            recall = metrics.get('recall', 0)
            st.metric("Recall", f"{recall:.1%}")
        
        with col4:
            f1 = metrics.get('f1', 0)
            st.metric("F1-Score", f"{f1:.1%}")
    
    @staticmethod
    def show_dataset_stats(df: pd.DataFrame) -> None:
        """
        Display dataset statistics
        
        Args:
            df: Dataset DataFrame
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Articles", len(df))
        
        with col2:
            if 'label' in df.columns:
                real_count = (df['label'] == 1).sum()
                st.metric("Real News", real_count)
        
        with col3:
            if 'label' in df.columns:
                fake_count = (df['label'] == 0).sum()
                st.metric("Fake News", fake_count)
        
        with col4:
            if 'text' in df.columns:
                avg_length = df['text'].str.len().mean()
                st.metric("Avg Text Length", f"{avg_length:.0f}")

class VisualizationComponents:
    """Components for creating visualizations"""
    
    @staticmethod
    def confidence_gauge(confidence: float, title: str = "Confidence") -> None:
        """
        Display a confidence gauge
        
        Args:
            confidence: Confidence value (0-1)
            title: Gauge title
        """
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def probability_chart(fake_prob: float, real_prob: float) -> None:
        """
        Display probability chart
        
        Args:
            fake_prob: Probability of fake news
            real_prob: Probability of real news
        """
        fig = go.Figure(data=[
            go.Bar(
                x=['Fake', 'Real'],
                y=[fake_prob * 100, real_prob * 100],
                marker_color=['red', 'green']
            )
        ])
        
        fig.update_layout(
            title='Prediction Probabilities',
            yaxis_title='Probability (%)',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def model_comparison_chart(results: Dict[str, Dict]) -> None:
        """
        Create model comparison chart
        
        Args:
            results: Dictionary of model results
        """
        models = []
        confidences = []
        predictions = []
        
        for model_name, result in results.items():
            if 'error' not in result:
                models.append(model_name.replace('_', ' ').title())
                confidences.append(result['confidence'] * 100)
                predictions.append(result['label'])
        
        if models:
            fig = px.bar(
                x=models,
                y=confidences,
                color=predictions,
                title="Model Comparison",
                labels={'x': 'Model', 'y': 'Confidence (%)', 'color': 'Prediction'},
                color_discrete_map={'Real': 'green', 'Fake': 'red'}
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

class InputComponents:
    """Components for user input"""
    
    @staticmethod
    def text_input_area(label: str = "Enter text to analyze:", height: int = 200) -> str:
        """
        Create a text input area
        
        Args:
            label: Input label
            height: Input height
            
        Returns:
            User input text
        """
        return st.text_area(
            label,
            height=height,
            placeholder="Paste or type the news article text here..."
        )
    
    @staticmethod
    def file_uploader_component() -> Optional[str]:
        """
        Create a file uploader component
        
        Returns:
            Uploaded file content as string or None
        """
        uploaded_file = st.file_uploader(
            "Upload a text file:",
            type=['txt', 'csv'],
            help="Upload a text file (.txt) or CSV file with news articles"
        )
        
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                return str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
                st.write("CSV file contents:")
                st.dataframe(df.head())
                
                if 'text' in df.columns:
                    selected_row = st.selectbox("Select row to analyze:", df.index)
                    return df.loc[selected_row, 'text']
        
        return None
    
    @staticmethod
    def news_search_inputs() -> Dict[str, Any]:
        """
        Create news search input components
        
        Returns:
            Dictionary with search parameters
        """
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_type = st.radio(
                "News source:",
                ["Top Headlines", "Search Articles", "Specific Sources"]
            )
        
        with col2:
            num_articles = st.slider("Number of articles:", 1, 20, 5)
        
        params = {'search_type': search_type, 'num_articles': num_articles}
        
        if search_type == "Top Headlines":
            params['country'] = st.selectbox("Country:", ['us', 'uk', 'ca', 'au', 'in'])
        
        elif search_type == "Search Articles":
            params['query'] = st.text_input(
                "Search query:", 
                placeholder="e.g., technology, politics, health"
            )
        
        elif search_type == "Specific Sources":
            # Mock source list - in real app, this would come from NewsAPI
            sources = ['cnn', 'bbc-news', 'reuters', 'associated-press', 'the-guardian-uk']
            params['sources'] = st.multiselect(
                "Select sources:",
                sources,
                default=sources[:3]
            )
        
        return params

class StatusComponents:
    """Components for displaying status information"""
    
    @staticmethod
    def show_loading_status(message: str = "Processing...") -> None:
        """
        Show loading status
        
        Args:
            message: Loading message
        """
        with st.spinner(message):
            pass
    
    @staticmethod
    def show_model_status(is_loaded: bool, model_count: int = 0) -> None:
        """
        Show model loading status
        
        Args:
            is_loaded: Whether models are loaded
            model_count: Number of models loaded
        """
        if is_loaded:
            st.success(f"✅ {model_count} ML models loaded successfully")
        else:
            st.warning("⚠️ Using fallback predictor (rule-based)")
    
    @staticmethod
    def show_api_status(is_connected: bool, api_name: str = "NewsAPI") -> None:
        """
        Show API connection status
        
        Args:
            is_connected: Whether API is connected
            api_name: Name of the API
        """
        if is_connected:
            st.success(f"🌐 {api_name} connected")
        else:
            st.info(f"📊 Using mock data ({api_name} not configured)")
    
    @staticmethod
    def show_error_message(error: str, suggestion: str = None) -> None:
        """
        Show error message with optional suggestion
        
        Args:
            error: Error message
            suggestion: Optional suggestion for fixing the error
        """
        st.error(f"❌ Error: {error}")
        if suggestion:
            st.info(f"💡 Suggestion: {suggestion}")

# Helper function to initialize all components
def initialize_app_components():
    """Initialize all app components and return component instances"""
    return {
        'prediction': PredictionDisplay(),
        'news': NewsDisplay(),
        'metrics': MetricsDisplay(),
        'viz': VisualizationComponents(),
        'input': InputComponents(),
        'status': StatusComponents()
    }