import os 
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('TMDB_API_KEY')
if not API_KEY:
    raise ValueError("A chave da API não foi encontrada, configure a variavel de ambiente TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

class TMDBAPIError(Exception):
    pass

def make_api_request(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_key'] = API_KEY
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise TMDBAPIError(f"Erro ao acessar a API do TMDB: {e}")
    

def get_movie_details(movie_id, language="pt-BR"):
    return make_api_request(f"/movie/{movie_id}", {"language": language})


def get_movie_credits(movie_id, language="pt-BR"):
    return make_api_request(f"/movie/{movie_id}/credits", {"language": language})


def get_movie_recommendations(movie_id, language="pt-BR", page=1):
    return make_api_request(f"/movie/{movie_id}/recommendations", 
                           {"language": language, "page": page})


def get_similar_movies(movie_id, language="pt-BR", page=1):
    return make_api_request(f"/movie/{movie_id}/similar", 
                           {"language": language, "page": page})


def search_movie(query, language="pt-BR", page=1):
    return make_api_request("/search/movie", 
                           {"query": query, "language": language, "page": page})

