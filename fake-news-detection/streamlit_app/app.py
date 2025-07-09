"""
Streamlit Application for Fake News Detection System
Interactive web interface with text analysis, real-time news fetching, and visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import sys
import os

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from prediction import FakeNewsPredictor, create_fallback_predictor
    from api_integration import NewsAPIClient, NewsProcessor
    from preprocessing import prepare_sample_data
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1e88e5;
    }
    .fake-news {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .real-news {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'predictor' not in st.session_state:
    with st.spinner('Loading prediction models...'):
        try:
            st.session_state.predictor = FakeNewsPredictor()
            if not st.session_state.predictor.is_ready():
                st.session_state.predictor = create_fallback_predictor()
                st.session_state.using_fallback = True
            else:
                st.session_state.using_fallback = False
        except Exception as e:
            st.session_state.predictor = create_fallback_predictor()
            st.session_state.using_fallback = True

if 'news_client' not in st.session_state:
    st.session_state.news_client = NewsAPIClient()

# Header
st.markdown('<h1 class="main-header">📰 Fake News Detection System</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.selectbox(
        "Choose a page:",
        ["Text Analysis", "Real-time News", "Model Comparison", "Data Insights"]
    )
    
    st.markdown("---")
    
    # Model information
    if st.session_state.using_fallback:
        st.warning("⚠️ Using fallback predictor (rule-based)")
    else:
        st.success("✅ ML models loaded successfully")
    
    # API status
    if st.session_state.news_client.use_mock_data:
        st.info("📊 Using mock news data")
    else:
        st.success("🌐 NewsAPI connected")

# Main content based on selected page
if page == "Text Analysis":
    st.markdown('<h2 class="section-header">📝 Text Analysis</h2>', unsafe_allow_html=True)
    
    # Text input options
    input_method = st.radio(
        "Choose input method:",
        ["Type/Paste Text", "Upload File"]
    )
    
    text_to_analyze = ""
    
    if input_method == "Type/Paste Text":
        text_to_analyze = st.text_area(
            "Enter news article text:",
            height=200,
            placeholder="Paste or type the news article text here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file:",
            type=['txt', 'csv']
        )
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                text_to_analyze = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
                st.write("CSV file contents:")
                st.dataframe(df.head())
                
                if 'text' in df.columns:
                    selected_row = st.selectbox("Select row to analyze:", df.index)
                    text_to_analyze = df.loc[selected_row, 'text']
    
    # Analysis
    if text_to_analyze:
        st.markdown("### Analysis Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Single prediction
            with st.spinner('Analyzing text...'):
                result = st.session_state.predictor.predict_single(text_to_analyze)
            
            # Display result
            if result['label'] == 'Fake':
                st.markdown(f"""
                <div class="metric-card fake-news">
                    <h3>🚨 Prediction: FAKE NEWS</h3>
                    <p><strong>Confidence:</strong> {result['confidence']:.2%}</p>
                    <p><strong>Fake Probability:</strong> {result['fake_probability']:.2%}</p>
                    <p><strong>Real Probability:</strong> {result['real_probability']:.2%}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card real-news">
                    <h3>✅ Prediction: REAL NEWS</h3>
                    <p><strong>Confidence:</strong> {result['confidence']:.2%}</p>
                    <p><strong>Fake Probability:</strong> {result['fake_probability']:.2%}</p>
                    <p><strong>Real Probability:</strong> {result['real_probability']:.2%}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Confidence gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = result['confidence'] * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Confidence"},
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
        
        # Model comparison (if multiple models available)
        if not st.session_state.using_fallback:
            with st.expander("🔍 Detailed Model Comparison"):
                try:
                    all_results = st.session_state.predictor.predict_with_all_models(text_to_analyze)
                    
                    comparison_data = []
                    for model_name, model_result in all_results.items():
                        if 'error' not in model_result:
                            comparison_data.append({
                                'Model': model_name.replace('_', ' ').title(),
                                'Prediction': model_result['label'],
                                'Confidence': f"{model_result['confidence']:.2%}",
                                'Fake Prob': f"{model_result['fake_probability']:.2%}",
                                'Real Prob': f"{model_result['real_probability']:.2%}"
                            })
                    
                    if comparison_data:
                        comparison_df = pd.DataFrame(comparison_data)
                        st.dataframe(comparison_df, use_container_width=True)
                        
                        # Ensemble prediction
                        try:
                            ensemble_result = st.session_state.predictor.get_ensemble_prediction(text_to_analyze)
                            st.markdown(f"""
                            **🎯 Ensemble Prediction:** {ensemble_result['label']} 
                            (Confidence: {ensemble_result['confidence']:.2%}, 
                            Models used: {ensemble_result['models_used']})
                            """)
                        except Exception as e:
                            st.error(f"Ensemble prediction failed: {e}")
                
                except Exception as e:
                    st.error(f"Model comparison failed: {e}")
        
        # Text statistics
        with st.expander("📊 Text Statistics"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Word Count", len(text_to_analyze.split()))
            with col2:
                st.metric("Character Count", len(text_to_analyze))
            with col3:
                st.metric("Sentence Count", text_to_analyze.count('.') + text_to_analyze.count('!') + text_to_analyze.count('?'))
            with col4:
                avg_word_length = np.mean([len(word) for word in text_to_analyze.split()])
                st.metric("Avg Word Length", f"{avg_word_length:.1f}")

elif page == "Real-time News":
    st.markdown('<h2 class="section-header">🌐 Real-time News Analysis</h2>', unsafe_allow_html=True)
    
    # News fetching options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        news_type = st.radio(
            "News source:",
            ["Top Headlines", "Search News", "Specific Sources"]
        )
    
    with col2:
        num_articles = st.slider("Number of articles:", 1, 20, 5)
    
    # Fetch news based on selection
    articles = []
    
    if news_type == "Top Headlines":
        country = st.selectbox("Country:", ['us', 'uk', 'ca', 'au', 'in'])
        if st.button("Fetch Headlines"):
            with st.spinner('Fetching headlines...'):
                articles = st.session_state.news_client.get_top_headlines(
                    country=country, 
                    page_size=num_articles
                ) or []
    
    elif news_type == "Search News":
        search_query = st.text_input("Search query:", placeholder="e.g., technology, politics, health")
        if search_query and st.button("Search News"):
            with st.spinner('Searching news...'):
                articles = st.session_state.news_client.search_news(
                    search_query, 
                    page_size=num_articles
                ) or []
    
    elif news_type == "Specific Sources":
        credible_sources = NewsProcessor.get_credible_sources()
        selected_sources = st.multiselect(
            "Select sources:",
            credible_sources,
            default=credible_sources[:3]
        )
        if selected_sources and st.button("Fetch from Sources"):
            sources_str = ','.join(selected_sources)
            with st.spinner('Fetching from sources...'):
                articles = st.session_state.news_client.get_news_by_source(
                    sources_str, 
                    page_size=num_articles
                ) or []
    
    # Display and analyze articles
    if articles:
        st.markdown(f"### 📰 Found {len(articles)} articles")
        
        # Analyze all articles
        analysis_results = []
        
        with st.spinner('Analyzing articles...'):
            for article in articles:
                formatted_article = NewsProcessor.format_article_for_display(article)
                text_content = formatted_article['full_text']
                
                if len(text_content) > 50:  # Only analyze articles with sufficient content
                    result = st.session_state.predictor.predict_single(text_content)
                    analysis_results.append({
                        'article': formatted_article,
                        'prediction': result
                    })
        
        # Summary statistics
        if analysis_results:
            fake_count = sum(1 for r in analysis_results if r['prediction']['label'] == 'Fake')
            real_count = len(analysis_results) - fake_count
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Articles", len(analysis_results))
            with col2:
                st.metric("Real News", real_count)
            with col3:
                st.metric("Fake News", fake_count)
            with col4:
                fake_percentage = (fake_count / len(analysis_results)) * 100
                st.metric("Fake %", f"{fake_percentage:.1f}%")
            
            # Individual article results
            st.markdown("### 📋 Article Analysis Results")
            
            for i, result in enumerate(analysis_results):
                article = result['article']
                prediction = result['prediction']
                
                with st.expander(f"{i+1}. {article['title'][:80]}..."):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Source:** {article['source']}")
                        st.markdown(f"**Author:** {article['author']}")
                        st.markdown(f"**Published:** {article['published_at']}")
                        st.markdown(f"**Description:** {article['description']}")
                        
                        if article['url']:
                            st.markdown(f"[Read full article]({article['url']})")
                    
                    with col2:
                        if prediction['label'] == 'Fake':
                            st.error(f"🚨 FAKE ({prediction['confidence']:.1%} confidence)")
                        else:
                            st.success(f"✅ REAL ({prediction['confidence']:.1%} confidence)")
                        
                        st.progress(prediction['confidence'])
                        
                        st.caption(f"Fake: {prediction['fake_probability']:.1%}")
                        st.caption(f"Real: {prediction['real_probability']:.1%}")

elif page == "Model Comparison":
    st.markdown('<h2 class="section-header">🤖 Model Comparison</h2>', unsafe_allow_html=True)
    
    if st.session_state.using_fallback:
        st.warning("⚠️ Model comparison not available with fallback predictor")
        st.info("To enable model comparison, please train the ML models first.")
    else:
        # Sample texts for comparison
        sample_texts = [
            "Scientists at Harvard University have published a peer-reviewed study showing promising results for a new cancer treatment.",
            "SHOCKING: This one weird trick will make you lose 50 pounds in one week! Doctors hate this secret!",
            "The Federal Reserve announced a 0.25% interest rate increase following their monthly meeting.",
            "BREAKING: Aliens confirmed to be living among us! Government finally admits decades-long cover-up!",
            "Local weather forecast predicts rain for the weekend with temperatures in the 70s.",
            "MIRACLE CURE: Grandmother's kitchen recipe cures diabetes, heart disease, and cancer instantly!"
        ]
        
        # Model performance metrics (would come from training)
        st.markdown("### 📊 Model Performance Metrics")
        
        # Mock performance data (in real scenario, this would be loaded from evaluation results)
        performance_data = {
            'Model': ['Logistic Regression', 'SVM', 'Random Forest'],
            'Accuracy': [0.87, 0.84, 0.91],
            'Precision': [0.85, 0.82, 0.89],
            'Recall': [0.88, 0.86, 0.92],
            'F1-Score': [0.86, 0.84, 0.90]
        }
        
        performance_df = pd.DataFrame(performance_data)
        
        # Performance comparison chart
        fig = px.bar(
            performance_df.melt(id_vars=['Model'], var_name='Metric', value_name='Score'),
            x='Model',
            y='Score',
            color='Metric',
            title='Model Performance Comparison',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Sample text predictions
        st.markdown("### 🧪 Sample Predictions")
        
        for i, text in enumerate(sample_texts):
            with st.expander(f"Sample {i+1}: {text[:60]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Text:** {text}")
                    
                    # Get predictions from all models
                    all_results = st.session_state.predictor.predict_with_all_models(text)
                    
                    results_data = []
                    for model_name, result in all_results.items():
                        if 'error' not in result:
                            results_data.append({
                                'Model': model_name.replace('_', ' ').title(),
                                'Prediction': result['label'],
                                'Confidence': result['confidence']
                            })
                    
                    if results_data:
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True)
                
                with col2:
                    # Confidence comparison chart
                    if results_data:
                        fig = px.bar(
                            results_df,
                            x='Model',
                            y='Confidence',
                            color='Prediction',
                            title='Prediction Confidence'
                        )
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)

elif page == "Data Insights":
    st.markdown('<h2 class="section-header">📈 Data Insights</h2>', unsafe_allow_html=True)
    
    # Load sample data for visualization
    sample_df = prepare_sample_data()
    
    st.markdown("### 📊 Sample Dataset Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(sample_df, use_container_width=True)
    
    with col2:
        # Label distribution
        label_counts = sample_df['label'].value_counts()
        fig = px.pie(
            values=label_counts.values,
            names=['Fake', 'Real'],
            title='Label Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Word clouds
    st.markdown("### ☁️ Word Clouds")
    
    fake_texts = sample_df[sample_df['label'] == 0]['text'].str.cat(sep=' ')
    real_texts = sample_df[sample_df['label'] == 1]['text'].str.cat(sep=' ')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Fake News Word Cloud**")
        try:
            fake_wordcloud = WordCloud(width=400, height=300, background_color='white').generate(fake_texts)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(fake_wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not generate word cloud: {e}")
    
    with col2:
        st.markdown("**Real News Word Cloud**")
        try:
            real_wordcloud = WordCloud(width=400, height=300, background_color='white').generate(real_texts)
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.imshow(real_wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Could not generate word cloud: {e}")
    
    # Text length analysis
    st.markdown("### 📏 Text Length Analysis")
    
    sample_df['text_length'] = sample_df['text'].str.len()
    sample_df['word_count'] = sample_df['text'].str.split().str.len()
    
    fig = px.box(
        sample_df,
        x='label',
        y='text_length',
        title='Text Length Distribution by Label'
    )
    fig.update_xaxis(ticktext=['Fake', 'Real'], tickvals=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Fake News Detection System v1.0 | Built with Streamlit</p>
    <p>⚠️ This system is for educational purposes. Always verify news from multiple reliable sources.</p>
</div>
""", unsafe_allow_html=True)