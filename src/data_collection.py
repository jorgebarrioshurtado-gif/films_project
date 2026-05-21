import requests
import time
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
if not api_key:
    raise ValueError("TMDB_API_KEY not found in environment variables")

# to test how it works and recall data from specific movies
def get_movie_details(tmdb_id, api_key = api_key):
    base = "https://api.themoviedb.org/3"
    url = f"{base}/movie/{tmdb_id}"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_movie_keywords(tmdb_id, api_key = api_key):
    base = "https://api.themoviedb.org/3"
    url = f"{base}/movie/{tmdb_id}/keywords"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    return response.json()


# to create the dataset
def enrich_film(tmdb_id, api_key = api_key):
    base = "https://api.themoviedb.org/3/movie"
    
    for attempt in range(3):  # try up to 3 times
        response = requests.get(f"{base}/{tmdb_id}", 
                               params={"api_key": api_key},
                               timeout=10)
        
        if response.status_code == 200:
            details = response.json()
            return {
                'tmdb_id': tmdb_id,
                'budget': details.get('budget'),
                'revenue': details.get('revenue')
            }
        elif response.status_code == 429:
            print(f"Rate limit hit — waiting 10 seconds")
            time.sleep(10)
        else:
            print(f"Error {response.status_code} on tmdb_id {tmdb_id}")
            return {'tmdb_id': tmdb_id, 'budget': None, 'revenue': None}
    
    # If all 3 attempts fail
    return {'tmdb_id': tmdb_id, 'budget': None, 'revenue': None}