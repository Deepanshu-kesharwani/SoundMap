
import streamlit as st
import requests
from streamlit_player import st_player
import pandas as pd
import os

st.set_page_config(page_title="SoundMap", page_icon="🎵", layout="wide")

# Load custom CSS (optional)
script_dir = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(script_dir, "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Top label
st.markdown("<h1 style='text-align:center;'>SoundMap</h1>", unsafe_allow_html=True)

# Search bar at the top (centered, minimal)
search_query = st.text_input("", placeholder="Type song or artist name...")

# Split layout
left, right = st.columns([1, 2])

if search_query:
    try:
        response = requests.post(
            "https://fastapi-backend-zkeu.onrender.com/search",
            json={"query": search_query}
        )

        if response.status_code == 200:
            result = response.json()

            # --- Left: Recommendations ---
            with left:
                st.markdown("### Recommended for You")
                user_recommendations = result.get("user_recommendations", [])
                if user_recommendations:
                    for rec in user_recommendations:
                        st.write(f"{rec['name']} (Playcount: {rec['playcount']})")
                else:
                    st.info("No personalized recommendations yet.")

                # Optionally, also show artist search results
                lastfm_results = result.get("lastfm", [])
                if lastfm_results:
                    st.markdown("#### Related Artists")
                    df = pd.DataFrame(lastfm_results)
                    st.dataframe(df, use_container_width=True)

            # --- Right: Now Playing (YouTube only) ---
            with right:
                st.markdown("### Now Playing")
                youtube_videos = result.get("youtube", [])
                if youtube_videos:
                    for video in youtube_videos:
                        st.markdown(f"<p class='video-title'>{video['title']}</p>", unsafe_allow_html=True)
                        st_player(f"https://www.youtube.com/watch?v={video['videoId']}")
                else:
                    st.info("No video results found.")

        else:
            st.error(f"Error: Received status code {response.status_code}")
            st.code(response.text)
    except Exception as e:
        st.error(f"Error making request: {str(e)}")
else:
    # Empty state
    with left:
        st.markdown("### Recommended for You")
        st.info("No personalized recommendations yet.")
    with right:
        st.markdown("### Now Playing")
        st.info("No song is playing.")