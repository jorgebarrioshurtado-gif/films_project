import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
if not api_key:
    raise ValueError("TMDB_API_KEY not found in environment variables")

base_url = "https://api.themoviedb.org/3"

def get_movie_details(tmdb_id):
    url = f"{base_url}/movie/{tmdb_id}"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_keywords(tmdb_id):
    url = f"{base_url}/movie/{tmdb_id}/keywords"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    return response.json()