import requests
from collections import defaultdict

API_KEY = 'bf48292768beea4e78cc070fc994f55c' 

def get_movie_data(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=pt-BR'
    response = requests.get(url)
    return response.json()

def get_movie_credits(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=pt-BR'
    response = requests.get(url)
    return response.json()

def analyze_movies(movie_ids):
    actor_count = defaultdict(int)
    genre_count = defaultdict(int)
    actor_revenue = defaultdict(float)

    for movie_id in movie_ids:
        data = get_movie_data(movie_id)
        credits = get_movie_credits(movie_id)

        # print(f"Resposta da API para o filme ID {movie_id}: {data}")

        # Processa os gêneros
        for genre in data.get('genres', []):
            genre_count[genre['name']] += 1

        # Processa a bilheteira
        revenue = data.get('revenue', 0)
        if revenue > 0:
            for actor in credits.get('cast', []):
                actor_count[actor['name']] += 1
                actor_revenue[actor['name']] += revenue

    # Top 5 Atores com Maior Bilheteira
    top_actors = sorted(actor_revenue.items(), key=lambda x: x[1], reverse=True)[:5]

    # Exibir resultados
    print("")
    print("Participação por Ator:", dict(actor_count))
    print("")
    print("Frequência de Gêneros:", dict(genre_count))
    print("")
    print("Top 5 Atores com Maior Bilheteira:", top_actors)
    print("")

if __name__ == "__main__":
    movie_ids = [550, 299536, 278]  # IDs de filmes válidos
    analyze_movies(movie_ids)