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
            movies = self._fetch_movies_from_api(genre_id)

            if not movies:
                return []

            filtered_movies = self._filter_valid_movies(movies)
            random.shuffle(filtered_movies)

            self.cache[genre_id] = filtered_movies
            return filtered_movies

        except requests.RequestException as error:
            print(f"TMDB request error: {error}")
            return []
        except ValueError as error:
            print(f"TMDB response error: {error}")
            return []
        except Exception as error:
            print(f"Unexpected movie fetcher error: {error}")
            return []

    def get_trending_movie(self) -> dict[str, Any] | None:
        try:
            url = f"{self.base_url}/trending/movie/day"
            params = {
                "api_key": self.api_key,
                "language": "ru-RU",
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ValueError("Invalid TMDB trending response format")

            results = data.get("results", [])

            if not isinstance(results, list):
                raise ValueError("Invalid TMDB trending results format")

            filtered_movies = self._filter_valid_movies(results)

            if not filtered_movies:
                return None

            return filtered_movies[0]

        except requests.RequestException as error:
            print(f"TMDB trending request error: {error}")
            return None
        except ValueError as error:
            print(f"TMDB trending response error: {error}")
            return None
        except Exception as error:
            print(f"Unexpected trending movie error: {error}")
            return None

    def get_weekly_trending_movie(self) -> dict[str, Any] | None:
        try:
            url = f"{self.base_url}/trending/movie/week"
            params = {
                "api_key": self.api_key,
                "language": "ru-RU",
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ValueError("Invalid TMDB weekly trending response format")

            results = data.get("results", [])

            if not isinstance(results, list):
                raise ValueError("Invalid TMDB weekly trending results format")

            filtered_movies = self._filter_valid_movies(results)

            if not filtered_movies:
                return None

            return filtered_movies[0]

        except requests.RequestException as error:
            print(f"TMDB weekly trending request error: {error}")
            return None
        except ValueError as error:
            print(f"TMDB weekly trending response error: {error}")
            return None
        except Exception as error:
            print(f"Unexpected weekly trending movie error: {error}")
            return None

    def _fetch_movies_from_api(self, genre_id: str) -> list[dict[str, Any]]:
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

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("Invalid TMDB response format")

        results = data.get("results", [])

        if not isinstance(results, list):
            raise ValueError("Invalid TMDB movie results format")

        return results

    def _filter_valid_movies(self, movies: list[dict[str, Any]]) -> list[dict[str, Any]]:
        valid_movies = []

        for movie in movies:
            title = movie.get("title")
            overview = movie.get("overview")

            if not title:
                continue

            if not overview:
                continue

            valid_movies.append(movie)

        return valid_movies

    def format_movie(self, movie: dict[str, Any]) -> dict[str, Any]:
        poster_path = movie.get("poster_path")
        release_date = movie.get("release_date") or "????"
        rating = movie.get("vote_average", 0)

        try:
            rating = round(float(rating), 1)
        except (TypeError, ValueError):
            rating = 0

        return {
            "title": movie.get("title", "No title"),
            "overview": movie.get("overview", "No description available"),
            "rating": rating,
            "year": release_date[:4],
            "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None,
        }