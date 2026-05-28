import streamlit as st

import pandas as pd

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))
from src.data_collection import load_details_cache, get_film_details, get_poster_url
from src.styles import load_css

load_css()

BASE_DIR = Path(__file__).resolve().parents[1]
file_path = BASE_DIR / "data" / "visualizations" / "streamlit_data.csv"

api_key = st.secrets["TMDB_API_KEY"]
details_cache = load_details_cache()

st.set_page_config(
    page_title="WhatToWatch",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.header("🔍 WhatToWatch Recommender")

st.write("Where the magic happens...")
st.markdown("""
<div style='
    background-color: rgba(255, 210, 166, 0.1);
    border-left: 3px solid #FFD2A6;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    color: #D8C3B3;
    font-size: 0.9rem;
'>
Note: Films with a 💜 pass the bechdel test
</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    data = pd.read_csv(file_path)

    return data

data = load_data()

# ---------------------------------------------------
# FUNCTIONS SECTION
# ---------------------------------------------------

def random_film(film, how_many = 1, data = data):
    searched_film = data[data["title_year"] == film]
    cluster = data.loc[data["title_year"] == film, "cluster"].iloc[0]

    candidates = data[
        (data["cluster"] == cluster) &
        (data["title_year"] != film)
    ]

    sampled = candidates.sample(n=how_many, random_state=None)
    
    info_film = []
    for  _, row in searched_film.iterrows():
        info_film.append({
            'title': row['title'],
            'tmdb_id': row['tmdb_id'],
            'imdb_id': row['imdb_id'],
            'year': row['year'],
            'imdb_rating': row['avg_rating'],
            "bechdel_rating" : row['bechdel_rating'],
            'imdb_url': f"https://www.imdb.com/title/{row['imdb_id']}/"
        })


    recommendations = []
    for _, row in sampled.iterrows():
        recommendations.append({
            'title': row['title'],
            'tmdb_id': row['tmdb_id'],
            'imdb_id': row['imdb_id'],
            'year': row['year'],
            'imdb_rating': row['avg_rating'],
            "bechdel_rating" : row['bechdel_rating'],
            'imdb_url': f"https://www.imdb.com/title/{row['imdb_id']}/"
        })
    return info_film, recommendations


def display_recommendations(recommended_films, details_cache = details_cache, api_key = api_key):
    cols = st.columns(3)
    
    for i, film in enumerate(recommended_films):
        with cols[i % 3]:
            # Fetch details for this specific film
            details = get_film_details(film['tmdb_id'], api_key, details_cache)
            poster_url = get_poster_url(details)
            
            if poster_url:
                st.image(poster_url, width='content')
            else:
                st.image("https://via.placeholder.com/342x513?text=No+Poster", 
                        width='content')
            
            st.markdown(f"**{film['title']}**")
            if film["bechdel_rating"] == "Pass":
                st.markdown(f"{film['year']} · ⭐ {film['imdb_rating']:.1f} · 💜")
            else:
                st.markdown(f"{film['year']} · ⭐ {film['imdb_rating']:.1f}")
            
            # Tagline if available
            tagline = details.get('tagline')
            if tagline:
                st.caption(f"*{tagline}*")
            
            # Overview in expander so it doesn't clutter the UI
            overview = details.get('overview')
            if overview:
                with st.expander("Overview"):
                    st.write(overview)
            
            # IMDb link
            st.link_button("View on IMDb", film['imdb_url'])

def display_film(film, details_cache=details_cache, api_key=api_key):

    details = get_film_details(film[0]['tmdb_id'], api_key, details_cache)
    poster_url = get_poster_url(details)

    col1, col2 = st.columns([1, 2])

    with col1:
        if poster_url:
            st.image(poster_url, width='content')

    with col2:
        st.title(film[0]['title'])

        if film[0]["bechdel_rating"] == "Pass":
            st.markdown(f"{film[0]['year']} · ⭐ {film[0]['imdb_rating']:.1f} · 💜")
        else:
            st.markdown(f"{film[0]['year']} · ⭐ {film[0]['imdb_rating']:.1f}")

        tagline = details.get('tagline')
        if tagline:
            st.caption(tagline)

        overview = details.get('overview')
        if overview:
            st.write(overview)

        st.link_button("View on IMDb", film[0]['imdb_url'])

# ---------------------------------------------------
# SEARCHBAR SECTION
# ---------------------------------------------------
film = st.selectbox("Choose a film", 
                    options = list(data["title_year"].unique()))

how_many = st.slider("How many recommendations?",
                              min_value = 1,
                               max_value = 9,
                               value = 3,
                              step = 1)

info_film, recommendations = random_film(film, how_many)


show_recommendations = st.button("Show recommendations 🔍")
if show_recommendations:
    st.subheader("Your film:")
    display_film(info_film)
    st.divider()
    st.subheader("Your recommendations:")
    display_recommendations(recommendations)