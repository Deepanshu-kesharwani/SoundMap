#!/usr/bin/env python3
"""
Demo script to show how the fake news detection system works
"""

def demo_fake_news_detection():
    """Demonstrate the fake news detection system"""
    print("🚀 FAKE NEWS DETECTION SYSTEM DEMO")
    print("=" * 50)
    
    # Simple predictor class
    class FakeNewsDetector:
        def __init__(self):
            self.fake_indicators = [
                'shocking', 'unbelievable', 'miracle', 'secret',
                'doctors hate', 'amazing discovery', 'this one trick',
                'breaking news', 'urgent', 'must read', 'viral', 
                'exposed', 'revealed', 'scientists stunned'
            ]
        
        def analyze(self, text):
            text_lower = text.lower()
            fake_score = sum(1 for keyword in self.fake_indicators if keyword in text_lower)
            is_fake = fake_score >= 2
            confidence = min(0.6 + fake_score * 0.1, 0.9) if is_fake else 0.6
            
            return {
                'text': text,
                'prediction': 'FAKE NEWS' if is_fake else 'REAL NEWS',
                'confidence': f"{confidence:.0%}",
                'fake_indicators': fake_score,
                'reasoning': f"Found {fake_score} fake news indicators"
            }
    
    detector = FakeNewsDetector()
    
    # Test cases
    test_articles = [
        {
            'title': 'Climate Research Published in Nature Journal',
            'content': 'A comprehensive study involving 50 research institutions has been published in Nature, showing new evidence about climate patterns in the Arctic region. The peer-reviewed research involved five years of data collection.'
        },
        {
            'title': 'SHOCKING Discovery That Will Change Everything!',
            'content': 'UNBELIEVABLE miracle cure discovered by local grandmother! This one trick that doctors HATE will amaze you! Scientists are STUNNED by this secret discovery!'
        },
        {
            'title': 'Technology Stock Market Update',
            'content': 'Technology stocks showed mixed performance this quarter with some companies exceeding earnings expectations while others faced challenges in supply chain management.'
        },
        {
            'title': 'URGENT: Must Read Breaking News!',
            'content': 'VIRAL discovery exposed! This shocking secret that they dont want you to know will change your life forever! Breaking news that doctors and scientists refuse to acknowledge!'
        }
    ]
    
    print("📰 Analyzing News Articles...")
    print("\n")
    
    for i, article in enumerate(test_articles, 1):
        print(f"Article {i}:")
        print(f"Title: {article['title']}")
        print(f"Content: {article['content'][:80]}...")
        
        # Analyze the full text (title + content)
        full_text = f"{article['title']} {article['content']}"
        result = detector.analyze(full_text)
        
        # Display results with colors (using emojis for visual appeal)
        if result['prediction'] == 'FAKE NEWS':
            print(f"🚨 RESULT: {result['prediction']} (Confidence: {result['confidence']})")
            print(f"⚠️  {result['reasoning']}")
        else:
            print(f"✅ RESULT: {result['prediction']} (Confidence: {result['confidence']})")
            print(f"ℹ️  {result['reasoning']}")
        
        print("-" * 60)
        print()
    
    print("📊 SYSTEM FEATURES:")
    print("✅ Real-time text analysis")
    print("✅ Confidence scoring") 
    print("✅ Keyword-based detection")
    print("✅ Interactive web interface")
    print("✅ Multiple ML models (when trained)")
    print("✅ News API integration")
    print("✅ Ensemble predictions")
    print("✅ Feature importance analysis")
    
    print("\n🔧 TECHNICAL COMPONENTS:")
    print("• Text preprocessing with NLTK")
    print("• TF-IDF vectorization")
    print("• Machine Learning models (LogReg, SVM, RandomForest)")
    print("• Streamlit web interface")
    print("• NewsAPI real-time integration")
    print("• Cross-validation and hyperparameter tuning")
    print("• Model persistence and loading")
    
    print("\n⚠️  IMPORTANT DISCLAIMERS:")
    print("• This is an educational demonstration")
    print("• Always verify news from multiple reliable sources")
    print("• ML models can have biases and false predictions")
    print("• Critical thinking remains essential")
    
    print("\n🚀 TO GET STARTED:")
    print("1. cd fake-news-detection")
    print("2. pip install -r ../requirements.txt")
    print("3. streamlit run streamlit_app/app.py")
    print("4. Open http://localhost:8502 in your browser")
    
    print("\n" + "=" * 50)
    print("✨ Demo completed! The system is ready to use.")
    print("=" * 50)

if __name__ == "__main__":
    demo_fake_news_detection()