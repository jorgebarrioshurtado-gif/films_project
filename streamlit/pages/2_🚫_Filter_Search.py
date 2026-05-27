import streamlit as st

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import sys
sys.path.append("../")  
from src.data_collection import load_details_cache, get_film_details, get_poster_url
from src.styles import load_css

load_css()

api_key = st.secrets["TMDB_API_KEY"]
details_cache = load_details_cache()

st.set_page_config(
    page_title="WhatToWatch",
    page_icon="🚫",
    layout="wide"
)

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.header("🚫 WhatToWatch Filter Search")

st.write("Try filtering to get some ideas about movies!")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

def load_data():

    data = pd.read_csv("../data/visualizations/streamlit_data.csv")

    return data

data = load_data()

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------
st.subheader("Filters")

col1, col2 = st.columns(2)

with col1:
    bechdel_test = st.radio("Bechdel test score 💜", 
                            options =["Pass", "No preference"])

with col2:
    time = st.pills(label = "Runtime ⏱️", 
                    options = ["< 60 min", "60-90 min", "90-120 min", "120-180 min", "> 180 min"], 
                    selection_mode = "multi")

col3, col4 = st.columns(2)

with col3:
    min_rating = st.slider("Minimum rating 💯",
                              min_value = 0.0,
                               max_value = 10.0,
                               value = 5.0,
                              step = 0.1)
    
with col4:
    selected_year = st.slider("Year for your film 📅",
                                min_value = data["year"].min(),
                                max_value = data["year"].max(),
                                value = (1990, 2020),
                                step = 1)

start_year, end_year = selected_year
    

#with col4:
    #min_runtime = st.slider("Minimum runtime",
                              #min_value = data["runtime_min"].min(),
                               #max_value = data["runtime_min"].max(),
                               #value = 100,
                              #step = 1)

# filtered_df = filtered_df[filtered_df["runtime_min"] >= min_runtime]

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------

filtered_df = data.copy()

if bechdel_test != "No preference":
    filtered_df = filtered_df[filtered_df["bechdel_rating"] == bechdel_test]

filtered_df = filtered_df[(filtered_df["year"] >= start_year) & (filtered_df["year"] <= end_year)]

filtered_df = filtered_df[filtered_df["avg_rating"] >= min_rating]

runtime_ranges = {
    "< 60 min": lambda x: x < 60,
    "60-90 min": lambda x: x.between(60, 90),
    "90-120 min": lambda x: x.between(90, 120),
    "120-180 min": lambda x: x.between(120, 180),
    "> 180 min": lambda x: x > 180
}

if time:
    runtime_mask = False
    
    for option in time:
        runtime_mask |= runtime_ranges[option](filtered_df["runtime_min"])

    filtered_df = filtered_df[runtime_mask]

if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

filtered_df = filtered_df.drop(columns = ["tmdb_id", "title", "year", "cluster"])

filtered_df["IMDb URL"] = filtered_df.apply(lambda x: f"https://www.imdb.com/title/{x['imdb_id']}/",
                                            axis = 1)  

filtered_df = filtered_df.rename(columns = {
    "imdb_id" : "IMDb ID",
    "title_year" : "Title",
    "runtime_min" : "Runtime",
    "avg_rating" : "Avg. Rating",
    "bechdel_rating" : "Bechdel score",
    "IMDb URL" : "IMDb URL"
})


show_recommendations = st.button("Show filter search 🚫")
if show_recommendations:
    st.dataframe(
        filtered_df,
        column_config={
            "IMDb URL": st.column_config.LinkColumn(
                "IMDb link",
                display_text="Open IMDb 🎬"
            )
        },
        hide_index=True,
        use_container_width=True
    )
