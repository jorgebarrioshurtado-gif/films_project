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


# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.header("📊 WhatToWatch Dashboard")