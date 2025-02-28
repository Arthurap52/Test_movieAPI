import requests

API_KEY = 'bf48292768beea4e78cc070fc994f55c' 

# Coleta os dados do filme atravez do ID passado.
def get_movie_recommendations(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&language=pt-BR&page=1"
    response = requests.get(url)
    data = response.json()

    recommendations = data.get('results', [])[:5]
    return recommendations

if __name__ == "__main__":
    movie_id = int(input("Digite o ID do filme: "))  # Entrada feita pelo usuario
    recommendations = get_movie_recommendations(movie_id)
    
    if recommendations:
        print("Recomendações de filmes:")
        for movie in recommendations:
            print(f"- {movie['title']} (ID: {movie['id']})")
    else:
        print("Nenhuma recomendação encontrada.")
