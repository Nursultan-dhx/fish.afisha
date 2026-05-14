import json
from pathlib import Path
from typing import Any


class StorageManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.save({})

    def load(self) -> dict[str, Any]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data: dict[str, Any]) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"Storage save error: {error}")


class FavoritesManager(StorageManager):
    def get_favorites(self, user_id: int) -> list[dict[str, Any]]:
        data = self.load()
        return data.get(str(user_id), [])

    def movie_exists(self, user_id: int, title: str) -> bool:
        user_favorites = self.get_favorites(user_id)

        return any(
            movie.get("title") == title
            for movie in user_favorites
        )

    def add_movie(self, user_id: int, movie: dict[str, Any]) -> bool:
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            data[user_key] = []

        movie_title = movie.get("title")

        if not movie_title:
            return False

        if self.movie_exists(user_id, movie_title):
            return False

        data[user_key].append(movie)
        self.save(data)
        return True

    def remove_movie_by_index(self, user_id: int, movie_index: int) -> bool:
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            return False

        user_favorites = data[user_key]

        if movie_index < 0 or movie_index >= len(user_favorites):
            return False

        user_favorites.pop(movie_index)
        self.save(data)
        return True

    def clear_favorites(self, user_id: int) -> bool:
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            return False

        data[user_key] = []
        self.save(data)
        return True