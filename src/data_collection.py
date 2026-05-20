import requests

from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
if not api_key:
    raise ValueError("TMDB_API_KEY not found in environment variables")

# to test how it works and recall data from specific movies
def get_movie_details(tmdb_id):
    BASE_URL = "https://api.themoviedb.org/3"
    url = f"{BASE_URL}/movie/{tmdb_id}"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_keywords(tmdb_id):
    BASE_URL = "https://api.themoviedb.org/3"
    url = f"{BASE_URL}/movie/{tmdb_id}/keywords"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    return response.json()


# to create the dataset
def enrich_film(tmdb_id, api_key):
    base = "https://api.themoviedb.org/3/movie"
    
    details = requests.get(f"{base}/{tmdb_id}", 
                          params={"api_key": api_key}).json()
    #keywords = requests.get(f"{base}/{tmdb_id}/keywords",
                           #params={"api_key": api_key}).json()
    
    return {
        'tmdb_id': tmdb_id,
        'budget': details.get('budget'),
        'revenue': details.get('revenue'),
        #'keywords': [k['name'] for k in keywords.get('keywords', [])]
    }