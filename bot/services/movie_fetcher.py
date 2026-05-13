import random
from typing import Any

import requests


class MovieFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.cache = {}

    def get_movies_by_genre(self, genre_id: str) -> list[dict[str, Any]]:
        if genre_id in self.cache:
            return self.cache[genre_id]

        try:
            url = f"{self.base_url}/discover/movie"
            params = {
                "api_key": self.api_key,
                "with_genres": genre_id,
                "language": "ru-RU",
                "sort_by": "popularity.desc",
                "vote_count.gte": 100,
                "page": 1,
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            movies = response.json().get("results", [])
            random.shuffle(movies)

            self.cache[genre_id] = movies
            return movies

        except requests.RequestException as error:
            print(f"TMDB request error: {error}")
            return []

    def format_movie(self, movie: dict[str, Any]) -> dict[str, Any]:
        poster_path = movie.get("poster_path")

        return {
            "title": movie.get("title", "No title"),
            "overview": movie.get("overview", "No description available"),
            "rating": round(movie.get("vote_average", 0), 1),
            "year": movie.get("release_date", "????")[:4],
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
        }