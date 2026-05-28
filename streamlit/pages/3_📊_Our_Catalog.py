import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.append("../")  
from src.data_collection import load_details_cache, get_film_details, get_poster_url
from src.styles import load_css

load_css()

api_key = st.secrets["TMDB_API_KEY"]
details_cache = load_details_cache()

st.set_page_config(
    page_title="WhatToWatch",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.header("📊 WhatToWatch Catalog")

st.write("What's in our catalog?")
# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    data = pd.read_csv("../data/visualizations/streamlit_data.csv")

    return data

data = load_data()

filtered_df = data.copy()
# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("Summary Statistics")

# total films
total_films = filtered_df["imdb_id"].nunique()

# from to
start_year = filtered_df["year"].min()
last_year = filtered_df["year"].max()

# Average Rating
avg_rating = round(filtered_df["avg_rating"].mean(), 2)

# Median runtime
median_runtime = filtered_df["runtime_min"].median() 

# the same for bechdel
# total films
b_total_films = filtered_df["imdb_id"][filtered_df["bechdel_rating"] == "Pass"].nunique()

# from to
b_start_year = filtered_df["year"][filtered_df["bechdel_rating"] == "Pass"].min()
b_last_year = filtered_df["year"][filtered_df["bechdel_rating"] == "Pass"].max()

# Average Rating
b_avg_rating = round(filtered_df["avg_rating"][filtered_df["bechdel_rating"] == "Pass"].mean(), 2)

# Median runtime
b_median_runtime = filtered_df["runtime_min"][filtered_df["bechdel_rating"] == "Pass"].median()


#Average price transactions
#average_transaction = round(filtered_df["Total"].mean(), 2)

#Best product line
#best_product_line = filtered_df["Product line"].value_counts().index[0]


#first row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Films:", total_films)

with col2:
    st.metric("Median Runtime:", f"{median_runtime:,.0f} mins")

with col3:
    st.metric("Total Films 💜*:", b_total_films)

with col4:
    st.metric("Median Runtime 💜:", f"{b_median_runtime:,.0f} mins")

#second row

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("Average Rating:", avg_rating)
    
with col6:
    st.metric("Years:", f"{start_year} - {last_year}")

with col7:
    st.metric("Average Rating 💜:", b_avg_rating)
    
with col8:
    st.metric("Years 💜 **:", f"{b_start_year} - {b_last_year}")

st.divider()
st.subheader("Best rated film:")

def info_best_films(film):
    info_film = []
    for  _, row in film.iterrows():
        info_film.append({
            'title': row['title'],
            'tmdb_id': row['tmdb_id'],
            'imdb_id': row['imdb_id'],
            'year': row['year'],
            'imdb_rating': row['avg_rating'],
            "bechdel_rating" : row['bechdel_rating'],
            'imdb_url': f"https://www.imdb.com/title/{row['imdb_id']}/"
        })
    return info_film

def display_films(film, details_cache=details_cache, api_key=api_key):

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

best_overall = filtered_df[filtered_df["avg_rating"] == data["avg_rating"].max()]
best_bechdel = data[
    (data["bechdel_rating"] == "Pass") &
    (data["avg_rating"] == data[data["bechdel_rating"] == "Pass"]["avg_rating"].max())
]

film_to_display = info_best_films(best_overall)
display_films(film_to_display)

st.subheader("Best rated film which passes the Bechdel test 💜:")
bechdel__film_to_display = info_best_films(best_bechdel)
display_films(bechdel__film_to_display)

st.divider()
st.caption("\\* Out of the 15.295 films of our catalog, we had the results of the Bechdel test for 6.605. Films that are not considered as a pass can be wether a fail or an unknown result.")
st.caption("\\*\\* We do not have information about the Bechdel test from 2021. This does not mean there have not been films that pass this test.")
st.caption("Bechel test is not a quality measure about a film, it is not a indicator of how feminist it is either. It is just a women representation measure.")
           


