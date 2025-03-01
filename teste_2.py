import sys
import argparse
from tmdb_api import (
    get_movie_details, get_movie_recommendations,
    get_similar_movies, search_movie, TMDBAPIError
)

# Constants
MAX_RECOMMENDATIONS = 5
MAX_OVERVIEW_LENGTH = 100
OVERVIEW_TRUNCATION_SUFFIX = "..."
OVERVIEW_DEFAULT = "Sem descrição disponível."
RATING_STAR_SCALE = 2
MAX_RATING = 10

# UI elements
SEPARATOR = "="*60
MOVIE_EMOJI = "📽️"
TITLE_EMOJI = "🎬"
STAR_EMOJI = "⭐"


# Busca pelo ID de um filme
def find_movie_id(movie_query):
    try:
        search_results = search_movie(movie_query)
        if search_results.get('total_results', 0) > 0:
            movie = search_results['results'][0]
            return movie['id'], movie['title']
        return None, None
    except TMDBAPIError as e:
        print(f"Erro ao pesquisar filme: {e}")
        return None, None


# Processa as recomendações de filmes
def get_recommendations(movie_id):
    try:
        recommendations = get_movie_recommendations(movie_id)
        movies = recommendations.get('results', [])
        
        if len(movies) < MAX_RECOMMENDATIONS:
            movies = _supplement_with_similar_movies(movie_id, movies)
        
        return movies[:MAX_RECOMMENDATIONS]
    except TMDBAPIError as e:
        print(f"Erro ao obter recomendações: {e}")
        return []


# Complementa com filmes similares
def _supplement_with_similar_movies(movie_id, current_movies):
    try:
        similar_movies = get_similar_movies(movie_id)
        similar_results = similar_movies.get('results', [])
        
        existing_ids = {movie['id'] for movie in current_movies}
        
        for movie in similar_results:
            if movie['id'] not in existing_ids and len(current_movies) < MAX_RECOMMENDATIONS:
                current_movies.append(movie)
                existing_ids.add(movie['id'])
        
        return current_movies
    except TMDBAPIError:
        return current_movies


# Exibe os detalhes do filme
def print_movie_details(movie):
    release_year = _extract_release_year(movie)
    rating = movie.get('vote_average', 0)
    
    print(f"{MOVIE_EMOJI}  {movie['title']} ({release_year})")
    print(f"   Avaliação: {STAR_EMOJI * int(rating/RATING_STAR_SCALE)} ({rating}/{MAX_RATING})")
    
    overview = movie.get('overview', OVERVIEW_DEFAULT)
    if overview:
        overview = _truncate_overview(overview)
        print(f"   {overview}")
    print()


# Processa a data de lançamento do filme
def _extract_release_year(movie):
    release_date = movie.get('release_date', '')
    if release_date:
        return release_date[:4]
    return 'N/A'


def _truncate_overview(overview):
    if len(overview) > MAX_OVERVIEW_LENGTH:
        return overview[:MAX_OVERVIEW_LENGTH - 3] + OVERVIEW_TRUNCATION_SUFFIX
    return overview


def main():
    args = _parse_arguments()
    
    movie_id, movie_title = _resolve_movie_identifier(args)
    if not movie_id:
        return 1
    
    try:
        if not movie_title:
            movie_data = get_movie_details(movie_id)
            movie_title = movie_data.get('title', f'Filme {movie_id}')
        
        _print_header(movie_title, movie_id)
        
        recommended_movies = get_recommendations(movie_id)
        
        if not recommended_movies:
            print("Não foram encontradas recomendações para este filme.")
            return 0
        
        _print_recommendations(recommended_movies)
        
    except TMDBAPIError as e:
        print(f"Erro ao acessar dados da API: {e}")
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1
    
    return 0


def _parse_arguments():
    parser = argparse.ArgumentParser(description='Sistema de Recomendação de Filmes')
    parser.add_argument('movie', nargs='*', help='Nome do filme para obter recomendações')
    parser.add_argument('--id', type=int, help='ID do filme no TMDB para obter recomendações')
    
    return parser.parse_args()


def _resolve_movie_identifier(args):
    movie_id = args.id
    movie_title = None
    
    if not movie_id and args.movie:
        movie_title_query = ' '.join(args.movie)
        movie_id, movie_title = find_movie_id(movie_title_query)
        
        if not movie_id:
            print(f"Filme '{movie_title_query}' não encontrado.")
            return None, None
    elif not movie_id:
        parser = argparse.ArgumentParser(description='Sistema de Recomendação de Filmes')
        parser.add_argument('movie', nargs='*', help='Nome do filme para obter recomendações')
        parser.add_argument('--id', type=int, help='ID do filme no TMDB para obter recomendações')
        parser.print_help()
        return None, None
    
    return movie_id, movie_title


# Exibe o header
def _print_header(movie_title, movie_id):
    print("\n" + SEPARATOR)
    print(f"{TITLE_EMOJI} RECOMENDAÇÕES COM BASE EM: {movie_title} (ID: {movie_id})")
    print(SEPARATOR + "\n")


# Exibe as recomendações
def _print_recommendations(recommended_movies):
    print(f"Encontradas {len(recommended_movies)} recomendações:\n")
    for i, movie in enumerate(recommended_movies, 1):
        print(f"{i}. ", end="")
        print_movie_details(movie)


if __name__ == "__main__":
    sys.exit(main())