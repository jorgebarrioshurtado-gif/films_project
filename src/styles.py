import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Hide Streamlit default menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    .stApp {
        background-color: #1E1A17;
        color: #F5E6D3;
    }

    .stButton > button {
        background-color: #E89B5F;
        color: #1E1A17;
        border: none;
        border-radius: 14px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #F2B880;
        color: black;
        transform: scale(1.02);
    }

    section[data-testid="stSidebar"] {
        background-color: #2A2522;
    }

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] {
        background-color: #322C28;
        color: #F5E6D3;
        border-radius: 10px;
    }

    h1, h2, h3 {
        color: #FFD2A6;
    }

    </style>
    """, unsafe_allow_html=True)