import requests
import json
import time
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
cache_file = BASE_DIR / "data" / "app" / "tmdb_details_cache.json"

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


def load_details_cache(cache_file = cache_file):
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}

def save_details_cache(cache, cache_file = cache_file):
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def get_film_details(tmdb_id, api_key, cache):
    tmdb_id_str = str(tmdb_id)
    
    # Already in cache — return immediately
    if tmdb_id_str in cache:
        return cache[tmdb_id_str]
    
    # Not in cache — call API
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{tmdb_id}",
            params={"api_key": api_key},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            details = {
                'poster_path': data.get('poster_path'),
                'tagline': data.get('tagline'),
                'overview': data.get('overview')
            }
        else:
            details = {
                'poster_path': None,
                'tagline': None,
                'overview': None
            }
    except Exception:
        details = {
            'poster_path': None,
            'tagline': None,
            'overview': None
        }
    
    # Store and persist regardless of success or failure
    cache[tmdb_id_str] = details
    save_details_cache(cache)
    
    return details

def get_poster_url(details, size='w500'):
    poster_path = details.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/{size}{poster_path}"
    return None