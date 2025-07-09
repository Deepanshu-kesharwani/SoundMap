# SoundMap

SoundMap is a comprehensive Python application platform featuring two main systems:

## 🎵 Music Recommendation System
A Python web application for audio exploration, music recommendation, and data visualization.  
It uses **Streamlit** for a modern, interactive UI, **FastAPI** for backend REST APIs, **Redis** for fast caching, and connects to the **YouTube** and **Last.fm** APIs for rich music and audio metadata.  
SoundMap provides personalized song recommendations, and allows you to play YouTube videos ad-free directly from the interface.

## 📰 Fake News Detection System
A complete machine learning system for detecting fake news using NLP techniques, real-time news verification, and an interactive web interface. Features multiple ML algorithms, real-time NewsAPI integration, ensemble predictions, and comprehensive visualizations.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)

---

## About

SoundMap enables users to search, analyze, and visualize music data by integrating with YouTube and Last.fm APIs.  
It provides a responsive UI built with Streamlit, supports fast and scalable API operations with FastAPI, and uses Redis to cache results for a smooth, real-time experience.  
SoundMap also features a recommendation engine that suggests songs based on your tastes, and allows you to play recommended YouTube videos ad-free within the app.

---

## Features

### 🎵 SoundMap Music System
- **Music Recommendation:** Get personalized song suggestions powered by Last.fm and YouTube data.
- **Ad-Free YouTube Playback:** Watch YouTube music videos without interruptions or ads directly in the Streamlit interface.
- **Music Search:** Search for songs, artists, or albums using the Last.fm and YouTube APIs.
- **Audio Visualization:** Visualize audio features, waveforms, and other metadata.
- **Streamlit UI:** Intuitive, real-time web interface for seamless user experience.
- **RESTful Backend:** FastAPI backend provides robust, scalable API endpoints.
- **Caching:** Redis-based caching for faster repeated queries and efficient data handling.
- **API Integration:** Easily configure your YouTube and Last.fm API keys.

### 📰 Fake News Detection System
- **🤖 Machine Learning Models:** Multiple ML algorithms (Logistic Regression, SVM, Random Forest)
- **📰 Real-time News Analysis:** Integration with NewsAPI for live news feeds  
- **🎯 Ensemble Predictions:** Combine multiple models for improved accuracy
- **📊 Interactive Dashboard:** Streamlit-based web interface with visualizations
- **☁️ Word Clouds:** Visual representation of fake vs real news patterns
- **📈 Performance Metrics:** Comprehensive model evaluation and comparison
- **🔍 Feature Analysis:** Understand which words/features influence predictions

---

## Screenshots

*(Add screenshots of the Streamlit UI, song recommendations, ad-free YouTube playback, and visualizations here.)*

---

## Installation

### Prerequisites

- Python 3.8+
- [Redis](https://redis.io/download) (running locally or remotely)
- YouTube Data API Key
- Last.fm API Key

### Steps

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Deepanshu-kesharwani/SoundMap.git
    cd SoundMap
    ```

2. **(Optional) Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start Redis server:**  
   Make sure Redis is running on `localhost:6379` or update the configuration.

---

## Configuration

### 🎵 SoundMap Music System

Before running the music app, set your API keys and Redis URL as environment variables or in a `.env` file at the project root:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
LASTFM_API_KEY=your_lastfm_api_key_here
REDIS_URL=redis://localhost:6379/0
```

Or set them in your shell session:

```bash
export YOUTUBE_API_KEY=your_youtube_api_key_here
export LASTFM_API_KEY=your_lastfm_api_key_here
export REDIS_URL=redis://localhost:6379/0
```

### 📰 Fake News Detection System

Optionally configure NewsAPI for real-time news fetching:

```
NEWS_API_KEY=your_news_api_key_here
```

The system works with mock data if NewsAPI is not configured.

---

## Usage

### 🎵 SoundMap Music System

**1. Start the FastAPI backend:**
```bash
uvicorn backend.main:app --reload
```
*(Assumes your FastAPI app is in `backend/main.py` as `app`)*

**2. Start the Streamlit UI:**
```bash
streamlit run frontend/app.py
```
*(Assumes your Streamlit app is in `frontend/app.py`)*

**3. Visit the Streamlit UI in your browser:**  
By default: http://localhost:8501

### 📰 Fake News Detection System

**1. Navigate to the fake news detection system:**
```bash
cd fake-news-detection
```

**2. Run the Streamlit application:**
```bash
streamlit run streamlit_app/app.py
```

**3. Access the application:**
- Fake News Detection: http://localhost:8502

### Quick Start Options

- **Music only**: Run `streamlit run frontend/app.py`
- **Fake news detection only**: Run `streamlit run fake-news-detection/streamlit_app/app.py`
- **Both systems**: Run both commands in separate terminals

---

## Examples

- **Get Song Recommendations:** Use the Streamlit interface to receive music suggestions tailored to your preferences, powered by the Last.fm and YouTube APIs.
- **Play Ad-Free YouTube Videos:** Select a recommended song to instantly watch its music video ad-free within the app.
- **Search and Visualize Music:** Search for any song or artist and visualize audio features, waveforms, and other metadata.
- **API endpoints:** Use FastAPI endpoints for programmatic access to music data, recommendations, and search results.

---

## Project Structure

```plaintext
SoundMap/
├── backend/
│   ├── main.py         # FastAPI app (API endpoints, data integration)
│   └── services.py  
├── frontend/
│   ├── app.py          # Streamlit UI (user interface, visualization)
│   └── styles.css  
├── fake-news-detection/     # Complete Fake News Detection System
│   ├── data/
│   │   ├── historical/      # Historical news datasets
│   │   └── processed/       # Processed training data
│   ├── models/
│   │   ├── trained_models/  # Saved ML models
│   │   └── evaluation/      # Model evaluation results
│   ├── src/
│   │   ├── preprocessing.py # Text preprocessing and feature extraction
│   │   ├── training.py      # Model training and hyperparameter tuning
│   │   ├── prediction.py    # Prediction engine and inference
│   │   └── api_integration.py # NewsAPI integration
│   ├── streamlit_app/
│   │   ├── app.py          # Main Streamlit application
│   │   ├── components/     # UI components
│   │   └── utils/          # Utility functions
│   ├── notebooks/          # Jupyter notebooks for analysis
│   ├── config.py           # Configuration settings
│   └── README.md           # Fake news detection documentation
├── requirements.txt        # Python dependencies (includes both systems)
├── README.md              # Project documentation
├── .env.example           # Example environment configuration
└── ...
```

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request


---

## FAQ

**Q:** What API keys do I need?  
**A:** You need a YouTube Data API key and a Last.fm API key.

**Q:** Can I run Redis on a different host/port?  
**A:** Yes! Set the `REDIS_URL` environment variable.

**Q:** What file formats are supported?  
**A:** YouTube links, and audio formats supported by your visualization code.

**Q:** Are YouTube videos really ad-free?  
**A:** Yes, videos are embedded and played without ads within the app interface.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

- **Author:** [Deepanshu Kesharwani](https://github.com/Deepanshu-kesharwani)
- **Repository:** [SoundMap](https://github.com/Deepanshu-kesharwani/SoundMap)

---

*Feel free to modify this README as your project evolves!*
