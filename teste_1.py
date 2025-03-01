import sys 
from collections import defaultdict
from tmdb_api import get_movie_credits, get_movie_details, TMDBAPIError

# Constants
TOP_CAST_LIMIT = 10
TOP_ACTORS_REPORT_LIMIT = 5
DEFAULT_MOVIE_IDS = [550, 680, 11, 24428, 299536]

# UI elements
SEPARATOR_FULL = "="*60
SEPARATOR_SECTION = "-"*60
REPORT_TITLE = " "*20 + "RELATÓRIO DE ANÁLISE DE FILMES"
ACTOR_SECTION_TITLE = "🎭 PARTICIPAÇÃO POR ATOR:"
GENRE_SECTION_TITLE = "🎬 FREQUÊNCIA DE GÊNEROS:"
REVENUE_SECTION_TITLE = "💰 TOP 5 ATORES COM MAIOR BILHETERIA:"
CHECKMARK = "✓"


def analyze_movies(movie_ids):
    actor_count = defaultdict(int)
    genre_count = defaultdict(int)
    actor_revenue = defaultdict(float)
    
    movies_processed = 0
    
    print(f"Analisando {len(movie_ids)} filmes...")
    
    for movie_id in movie_ids:
        try:
            data = get_movie_details(movie_id)
            
            if _is_movie_not_found(data):
                print(f"Aviso: Filme ID {movie_id} não encontrado. Pulando.")
                continue
                
            credits = get_movie_credits(movie_id)
            
            _process_movie_genres(data, genre_count)
            _process_movie_actors(credits, data, actor_count, actor_revenue)
            
            movies_processed += 1
            _print_processing_status(data, movie_id)
            
        except TMDBAPIError as e:
            print(f"Erro ao processar filme {movie_id}: {e}")
        except Exception as e:
            print(f"Erro inesperado ao processar filme {movie_id}: {e}")
    
    top_actors = _get_top_revenue_actors(actor_revenue)
    
    return actor_count, dict(genre_count), top_actors


def _is_movie_not_found(data):
    return 'success' in data and data['success'] is False


# Processa a contagem dos generos  
def _process_movie_genres(data, genre_count):
    for genre in data.get('genres', []):
        genre_count[genre['name']] += 1


# Processa a contagem dos atores
def _process_movie_actors(credits, data, actor_count, actor_revenue):
    revenue = data.get('revenue', 0)
    
    for actor in credits.get('cast', [])[:TOP_CAST_LIMIT]:
        actor_name = actor['name']
        actor_count[actor_name] += 1
        
        if revenue > 0:
            actor_revenue[actor_name] += revenue / TOP_CAST_LIMIT


# Processa a confirmação de status do filme
def _print_processing_status(data, movie_id):
    title = data.get('title', f'Filme {movie_id}')
    print(f"{CHECKMARK} Processado: {title} (ID: {movie_id})")


# Processa os 5 atores com maior bilheteria
def _get_top_revenue_actors(actor_revenue):
    return sorted(
        actor_revenue.items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:TOP_ACTORS_REPORT_LIMIT]


def format_currency(value):
    return f"${value:,.2f}"


# Exibe os resultados
def print_results(actor_count, genre_count, top_actors):
    _print_report_header()
    _print_actor_participation(actor_count)
    _print_genre_frequency(genre_count)
    _print_top_revenue_actors(top_actors)
    _print_report_footer()


# Exibe o header 
def _print_report_header():
    print("\n" + SEPARATOR_FULL)
    print(REPORT_TITLE)
    print(SEPARATOR_FULL)


# Exibe a participação por ator
def _print_actor_participation(actor_count):
    print("\n" + ACTOR_SECTION_TITLE)
    print(SEPARATOR_SECTION)
    
    sorted_actors = sorted(actor_count.items(), key=lambda x: x[1], reverse=True)
    for actor, count in sorted_actors:
        print(f"• {actor}: {count} filme(s)")


# Exibe a frequencia dos genero
def _print_genre_frequency(genre_count):
    print("\n" + GENRE_SECTION_TITLE)
    print(SEPARATOR_SECTION)
    
    sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
    for genre, count in sorted_genres:
        print(f"• {genre}: {count} ocorrência(s)")


# Exibe os top atores com maior bilheteria
def _print_top_revenue_actors(top_actors):
    print("\n" + REVENUE_SECTION_TITLE)
    print(SEPARATOR_SECTION)
    
    for i, (actor, revenue) in enumerate(top_actors, 1):
        print(f"{i}. {actor}: {format_currency(revenue)}")


# Exibe o footer
def _print_report_footer():
    print("\n" + SEPARATOR_FULL + "\n")


def main():
    movie_ids = _parse_movie_ids()
    if not movie_ids:
        return 1
    
    try:
        actor_count, genre_count, top_actors = analyze_movies(movie_ids)
        print_results(actor_count, genre_count, top_actors)
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        return 1
        
    return 0


def _parse_movie_ids():
    if len(sys.argv) > 1:
        try:
            return [int(id.strip()) for id in sys.argv[1:]]
        except ValueError:
            print("Erro: IDs de filmes devem ser números inteiros.")
            return None
    else:
        return DEFAULT_MOVIE_IDS


if __name__ == "__main__":
    sys.exit(main())