import streamlit as st

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.styles import load_css

load_css()

st.set_page_config(
    page_title="WhatToWatch",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<div style='text-align:center; padding: 2rem 0 3rem 0;'>

<h1 style='
color:#FFD2A6;
font-size:4rem;
margin-bottom:0.5rem;
'>
🎬 WhatToWatch
</h1>

<p style='
color:#D8C3B3;
font-size:1.2rem;
'>
Next favourite movie awaits here
</p>

</div>
""", unsafe_allow_html=True)

st.write("""This project is born with three main purposes:""")
st.markdown("- Women underrepresentation is a real concern.")
st.markdown("- Genres do not give us any relevant information about the kind of film we are watching.")
st.markdown("- Everyone has a favourite film and want to find similar films 😎")
st.divider()
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <a href="/WhatToWatch" target="_self" style="text-decoration:none;">
        <div class="nav-card">
            <div class="icon">🔍</div>
            <div class="title">Recommender</div>
            <div class="subtitle">
                Discover movies based on your taste
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <a href="/Filter_Search" target="_self" style="text-decoration:none;">
        <div class="nav-card">
            <div class="icon">🚫</div>
            <div class="title">Filter Search</div>
            <div class="subtitle">
                No ideas today? Find movies by filtering!
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <a href="/Our_Catalog" target="_self" style="text-decoration:none;">
        <div class="nav-card">
            <div class="icon">📊</div>
            <div class="title">Our Catalog</div>
            <div class="subtitle">
                Find some data about our catalog
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
            
/* Navigation cards */
.nav-card {
    background: #2A2522;
    padding: 2rem;
    border-radius: 20px;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    cursor: pointer;
            
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);

    transition: all 0.3s ease;

    border: 1px solid rgba(255,255,255,0.05);
}


/* Hover animation */
.nav-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow:
        0 12px 30px rgba(232,155,95,0.18);
    border: 1px solid #E89B5F;
}
/* Icon */
.icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* Title */
.title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #FFD2A6;
    margin-bottom: 0.5rem;
}

/* Subtitle */
.subtitle {
    color: #D8C3B3;
    font-size: 1rem;
    line-height: 1.5;
}

/* Bigger buttons */
.stPageLink a {
    background-color: #E89B5F;
    color: #1E1A17 !important;

    padding: 0.7rem 1.4rem;
    border-radius: 12px;

    text-decoration: none;
    font-weight: 700;

    display: inline-block;
    margin-top: 1rem;

    transition: 0.3s ease;
}

/* Button hover */
.stPageLink a:hover {
    background-color: #F2B880;
    transform: scale(1.03);
}

</style>
""", unsafe_allow_html=True)