import json
from pathlib import Path
from typing import Any


class StorageManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
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
    def add_movie(self, user_id: int, movie: dict[str, Any]) -> bool:
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            data[user_key] = []

        movie_titles = [item["title"] for item in data[user_key]]

        if movie["title"] in movie_titles:
            return False

        data[user_key].append(movie)
        self.save(data)
        return True

    def get_favorites(self, user_id: int) -> list[dict[str, Any]]:
        data = self.load()
        return data.get(str(user_id), [])

    def remove_movie_by_index(self, user_id: int, movie_index: int) -> bool:
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            return False

        if movie_index < 0 or movie_index >= len(data[user_key]):
            return False

        data[user_key].pop(movie_index)
        self.save(data)
        return True