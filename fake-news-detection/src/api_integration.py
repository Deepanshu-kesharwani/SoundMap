"""
API Integration Module for Real-time News Fetching
Handles NewsAPI integration with error handling and rate limiting
"""

import requests
import time
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta
import json

class NewsAPIClient:
    """Client for fetching news from NewsAPI"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize NewsAPI client
        
        Args:
            api_key: NewsAPI key (if None, tries to get from environment)
        """
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        if not self.api_key or self.api_key == 'your_news_api_key_here':
            print("Warning: NewsAPI key not provided. Using mock data.")
            self.use_mock_data = True
        else:
            self.use_mock_data = False
        
        self.base_url = "https://newsapi.org/v2"
        self.last_request_time = 0
        self.min_request_interval = 1  # Minimum seconds between requests
        
    def _rate_limit(self):
        """Implement basic rate limiting"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict) -> Optional[Dict]:
        """
        Make API request with error handling
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            API response or None if error
        """
        if self.use_mock_data:
            return self._get_mock_data(endpoint, params)
        
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        params['apiKey'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'error':
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return None
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def _get_mock_data(self, endpoint: str, params: Dict) -> Dict:
        """
        Generate mock data when API key is not available
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            Mock API response
        """
        if endpoint == "everything":
            return {
                "status": "ok",
                "totalResults": 4,
                "articles": [\n                    {\n                        "source": {"id": "cnn", "name": "CNN"},\n                        "author": "John Doe",\n                        "title": "Scientists Discover New Species in Deep Ocean",\n                        "description": "Marine biologists have identified a new species of fish in the Mariana Trench.",\n                        "url": "https://example.com/news1",\n                        "urlToImage": "https://example.com/image1.jpg",\n                        "publishedAt": "2024-01-15T10:30:00Z",\n                        "content": "Marine biologists working in the Mariana Trench have made an exciting discovery..."\n                    },\n                    {\n                        "source": {"id": "bbc", "name": "BBC News"},\n                        "author": "Jane Smith",\n                        "title": "Global Climate Summit Reaches Historic Agreement",\n                        "description": "World leaders agree on new climate action framework.",\n                        "url": "https://example.com/news2",\n                        "urlToImage": "https://example.com/image2.jpg",\n                        "publishedAt": "2024-01-15T08:15:00Z",\n                        "content": "In a historic moment for climate action, world leaders have reached consensus..."\n                    },\n                    {\n                        "source": {"id": "reuters", "name": "Reuters"},\n                        "author": "Mike Johnson",\n                        "title": "Technology Stock Market Hits New Records",\n                        "description": "Major tech companies see significant gains in trading.",\n                        "url": "https://example.com/news3",\n                        "urlToImage": "https://example.com/image3.jpg",\n                        "publishedAt": "2024-01-15T06:45:00Z",\n                        "content": "Technology stocks surged to new heights today as investors showed confidence..."\n                    },\n                    {\n                        "source": {"id": "fox-news", "name": "Fox News"},\n                        "author": "Sarah Wilson",\n                        "title": "SHOCKING: Local Grandmother's Secret Recipe Cures Everything!",\n                        "description": "Amazing discovery that doctors don't want you to know about!",\n                        "url": "https://example.com/news4",\n                        "urlToImage": "https://example.com/image4.jpg",\n                        "publishedAt": "2024-01-15T05:20:00Z",\n                        "content": "This one weird trick discovered by a grandmother will shock you! Doctors hate this secret..."\n                    }\n                ]\n            }\n        \n        elif endpoint == "top-headlines":\n            return {\n                "status": "ok",\n                "totalResults": 3,\n                "articles": [\n                    {\n                        "source": {"id": "associated-press", "name": "Associated Press"},\n                        "author": "AP News",\n                        "title": "Breaking: International Trade Agreement Signed",\n                        "description": "Major economies reach new trade deal.",\n                        "url": "https://example.com/headline1",\n                        "urlToImage": "https://example.com/headline1.jpg",\n                        "publishedAt": "2024-01-15T12:00:00Z",\n                        "content": "Government officials from major economies have successfully negotiated..."\n                    },\n                    {\n                        "source": {"id": "the-guardian", "name": "The Guardian"},\n                        "author": "Guardian Reporter",\n                        "title": "Medical Breakthrough in Cancer Research",\n                        "description": "Researchers announce promising new treatment approach.",\n                        "url": "https://example.com/headline2",\n                        "urlToImage": "https://example.com/headline2.jpg",\n                        "publishedAt": "2024-01-15T11:30:00Z",\n                        "content": "A team of international researchers has announced a significant breakthrough..."\n                    },\n                    {\n                        "source": {"id": "daily-mail", "name": "Daily Mail"},\n                        "author": "Mail Reporter",\n                        "title": "UNBELIEVABLE: Man Claims to Have Found Fountain of Youth!",\n                        "description": "Local man says he's discovered the secret to eternal life in his backyard.",\n                        "url": "https://example.com/headline3",\n                        "urlToImage": "https://example.com/headline3.jpg",\n                        "publishedAt": "2024-01-15T09:15:00Z",\n                        "content": "In an unbelievable turn of events, a local man claims to have discovered..."\n                    }\n                ]\n            }\n        \n        return {"status": "ok", "totalResults": 0, "articles": []}\n    \n    def search_news(self, \n                   query: str, \n                   language: str = 'en',\n                   sort_by: str = 'publishedAt',\n                   page_size: int = 20,\n                   from_date: str = None) -> Optional[List[Dict]]:\n        \"\"\"\n        Search for news articles\n        \n        Args:\n            query: Search query\n            language: Language code\n            sort_by: Sort order ('relevancy', 'popularity', 'publishedAt')\n            page_size: Number of articles to return\n            from_date: From date (YYYY-MM-DD format)\n            \n        Returns:\n            List of news articles or None if error\n        \"\"\"\n        if not from_date:\n            # Default to last 7 days\n            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')\n        \n        params = {\n            'q': query,\n            'language': language,\n            'sortBy': sort_by,\n            'pageSize': page_size,\n            'from': from_date\n        }\n        \n        response = self._make_request('everything', params)\n        \n        if response and response.get('status') == 'ok':\n            return response.get('articles', [])\n        \n        return None\n    \n    def get_top_headlines(self, \n                         country: str = 'us',\n                         category: str = None,\n                         page_size: int = 20) -> Optional[List[Dict]]:\n        \"\"\"\n        Get top headlines\n        \n        Args:\n            country: Country code\n            category: News category\n            page_size: Number of articles to return\n            \n        Returns:\n            List of top headlines or None if error\n        \"\"\"\n        params = {\n            'country': country,\n            'pageSize': page_size\n        }\n        \n        if category:\n            params['category'] = category\n        \n        response = self._make_request('top-headlines', params)\n        \n        if response and response.get('status') == 'ok':\n            return response.get('articles', [])\n        \n        return None\n    \n    def get_news_by_source(self, \n                          sources: str,\n                          page_size: int = 20) -> Optional[List[Dict]]:\n        \"\"\"\n        Get news from specific sources\n        \n        Args:\n            sources: Comma-separated source IDs\n            page_size: Number of articles to return\n            \n        Returns:\n            List of news articles or None if error\n        \"\"\"\n        params = {\n            'sources': sources,\n            'pageSize': page_size\n        }\n        \n        response = self._make_request('everything', params)\n        \n        if response and response.get('status') == 'ok':\n            return response.get('articles', [])\n        \n        return None\n\nclass NewsProcessor:\n    \"\"\"Process and format news articles for fake news detection\"\"\"\n    \n    @staticmethod\n    def extract_text_content(article: Dict) -> str:\n        \"\"\"\n        Extract text content from news article\n        \n        Args:\n            article: News article dictionary\n            \n        Returns:\n            Combined text content\n        \"\"\"\n        title = article.get('title', '') or ''\n        description = article.get('description', '') or ''\n        content = article.get('content', '') or ''\n        \n        # Combine title, description, and content\n        full_text = f\"{title} {description} {content}\".strip()\n        \n        return full_text\n    \n    @staticmethod\n    def format_article_for_display(article: Dict) -> Dict:\n        \"\"\"\n        Format article for display in UI\n        \n        Args:\n            article: Raw news article\n            \n        Returns:\n            Formatted article dictionary\n        \"\"\"\n        return {\n            'title': article.get('title', 'No title'),\n            'source': article.get('source', {}).get('name', 'Unknown source'),\n            'author': article.get('author', 'Unknown author'),\n            'description': article.get('description', 'No description available'),\n            'url': article.get('url', ''),\n            'image_url': article.get('urlToImage', ''),\n            'published_at': article.get('publishedAt', ''),\n            'content': article.get('content', ''),\n            'full_text': NewsProcessor.extract_text_content(article)\n        }\n    \n    @staticmethod\n    def filter_articles_by_length(articles: List[Dict], min_length: int = 50) -> List[Dict]:\n        \"\"\"\n        Filter articles by minimum text length\n        \n        Args:\n            articles: List of articles\n            min_length: Minimum text length\n            \n        Returns:\n            Filtered list of articles\n        \"\"\"\n        filtered = []\n        \n        for article in articles:\n            text_content = NewsProcessor.extract_text_content(article)\n            if len(text_content) >= min_length:\n                filtered.append(article)\n        \n        return filtered\n    \n    @staticmethod\n    def get_credible_sources() -> List[str]:\n        \"\"\"\n        Get list of generally credible news sources\n        \n        Returns:\n            List of credible source IDs\n        \"\"\"\n        return [\n            'associated-press', 'bbc-news', 'cnn', 'reuters', \n            'the-guardian-uk', 'the-new-york-times', 'the-washington-post',\n            'npr', 'abc-news', 'cbs-news', 'nbc-news'\n        ]\n    \n    @staticmethod\n    def get_questionable_sources() -> List[str]:\n        \"\"\"\n        Get list of potentially questionable news sources\n        \n        Returns:\n            List of questionable source IDs\n        \"\"\"\n        return [\n            'breitbart-news', 'infowars', 'natural-news',\n            'the-daily-mail', 'fox-news'  # Note: These are examples\n        ]\n\ndef create_news_fetcher(api_key: str = None) -> NewsAPIClient:\n    \"\"\"\n    Create a news fetcher instance\n    \n    Args:\n        api_key: NewsAPI key\n        \n    Returns:\n        NewsAPIClient instance\n    \"\"\"\n    return NewsAPIClient(api_key)\n\nif __name__ == \"__main__\":\n    # Demo news fetching\n    print(\"Initializing news client...\")\n    client = NewsAPIClient()\n    \n    print(\"\\nFetching top headlines...\")\n    headlines = client.get_top_headlines(page_size=5)\n    \n    if headlines:\n        print(f\"Found {len(headlines)} headlines:\")\n        for i, article in enumerate(headlines, 1):\n            formatted = NewsProcessor.format_article_for_display(article)\n            print(f\"\\n{i}. {formatted['title']}\")\n            print(f\"   Source: {formatted['source']}\")\n            print(f\"   Author: {formatted['author']}\")\n            print(f\"   Text length: {len(formatted['full_text'])} characters\")\n    else:\n        print(\"No headlines found\")\n    \n    print(\"\\nSearching for technology news...\")\n    tech_news = client.search_news('technology', page_size=3)\n    \n    if tech_news:\n        print(f\"Found {len(tech_news)} technology articles:\")\n        for i, article in enumerate(tech_news, 1):\n            formatted = NewsProcessor.format_article_for_display(article)\n            print(f\"\\n{i}. {formatted['title']}\")\n            print(f\"   Description: {formatted['description'][:100]}...\")\n    else:\n        print(\"No technology news found\")\n    \n    print(\"\\nNews fetching demo completed!\")