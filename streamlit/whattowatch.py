import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import requests
import sys
sys.path.append("../")  
from src.data_collection import load_details_cache, get_film_details, get_poster_url

api_key = st.secrets["TMDB_API_KEY"]
details_cache = load_details_cache()


# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.title("WhatToWatch")
st.write("""This project is born ...""")

st.divider()

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    data = pd.read_csv("../data/visualizations/streamlit_data.csv")

    return data

data = load_data()

# ---------------------------------------------------
# FUNCTIONS SECTION
# ---------------------------------------------------

def random_film(film, how_many = 1, data = data):
    cluster = data.loc[data["title_year"] == film, "cluster"].iloc[0]

    candidates = data[
        (data["cluster"] == cluster) &
        (data["title_year"] != film)
    ]

    sampled = candidates.sample(n=how_many, random_state=None)

    recommendations = []
    for _, row in sampled.iterrows():
        recommendations.append({
            'title': row['title'],
            'tmdb_id': row['tmdb_id'],
            'imdb_id': row['imdb_id'],
            'year': row['year'],
            'imdb_rating': row['avg_rating'],
            'imdb_url': f"https://www.imdb.com/title/{row['imdb_id']}/"
        })
    return recommendations


def display_recommendations(recommended_films, details_cache = details_cache, api_key = api_key):
    cols = st.columns(3)
    
    for i, film in enumerate(recommended_films):
        with cols[i % 3]:
            # Fetch details for this specific film
            details = get_film_details(film['tmdb_id'], api_key, details_cache)
            poster_url = get_poster_url(details)
            
            if poster_url:
                st.image(poster_url, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/342x513?text=No+Poster", 
                        use_container_width=True)
            
            st.markdown(f"**{film['title']}**")
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



# ---------------------------------------------------
# SEARCHBAR SECTION
# ---------------------------------------------------
film = st.selectbox("Choose a film", 
                    options = list(data["title_year"].unique()))

how_many = st.slider("How many recommendations?",
                              min_value = 1,
                               max_value = 10,
                               value = 3,
                              step = 1)

recommendations = random_film(film, how_many)


show_recommendations = st.button("Show recommendations 🔎")
if show_recommendations:
    #st.write(recommendations)
    display_recommendations(recommendations)





# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

# How many recommendations

