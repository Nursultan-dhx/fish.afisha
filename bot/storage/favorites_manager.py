import json
from pathlib import Path
from typing import Any


class StorageManager:
    """
    Base class for JSON file storage.

    This class provides common file operations:
    - creating a file if it does not exist;
    - loading data from JSON;
    - saving data to JSON;
    - handling file and JSON errors safely.

    FavoritesManager inherits from this class, which demonstrates
    inheritance as an advanced OOP concept.
    """

    def __init__(self, file_path: str):
        """
        Initialize storage manager.

        Args:
            file_path: Path to the JSON storage file.
        """
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Create the JSON file and parent directory if they do not exist.
        """
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.save({})

    def load(self) -> dict[str, Any]:
        """
        Load data from JSON file.

        Returns:
            Dictionary with stored data. Returns an empty dictionary if
            the file does not exist, is empty, or contains invalid JSON.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                if not isinstance(data, dict):
                    return {}

                return data

        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save(self, data: dict[str, Any]) -> None:
        """
        Save data to JSON file.

        Args:
            data: Dictionary that should be written to the JSON file.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"Storage save error: {error}")


class FavoritesManager(StorageManager):
    """
    Manages users' favorite movies.

    This class is responsible for:
    - adding movies to favorites;
    - checking if a movie already exists;
    - reading a user's favorite movies;
    - removing movies by index;
    - clearing all favorites for a user.

    Data is stored in JSON format using the methods inherited
    from StorageManager.
    """

    def get_favorites(self, user_id: int) -> list[dict[str, Any]]:
        """
        Get favorite movies for a specific user.

        Args:
            user_id: Telegram user ID.

        Returns:
            List of favorite movies. Returns an empty list if user has
            no saved movies.
        """
        data = self.load()
        return data.get(str(user_id), [])

    def movie_exists(self, user_id: int, title: str) -> bool:
        """
        Check whether a movie already exists in user's favorites.

        Args:
            user_id: Telegram user ID.
            title: Movie title.

        Returns:
            True if movie already exists, otherwise False.
        """
        user_favorites = self.get_favorites(user_id)

        return any(
            movie.get("title") == title
            for movie in user_favorites
        )

    def add_movie(self, user_id: int, movie: dict[str, Any]) -> bool:
        """
        Add movie to user's favorites.

        Args:
            user_id: Telegram user ID.
            movie: Movie dictionary with title, year, rating and overview.

        Returns:
            True if movie was added successfully.
            False if movie is invalid or already exists.
        """
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
        """
        Remove movie from user's favorites by index.

        Args:
            user_id: Telegram user ID.
            movie_index: Index of the movie in the user's favorites list.

        Returns:
            True if movie was removed successfully.
            False if user or index does not exist.
        """
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
        """
        Remove all favorite movies for a specific user.

        Args:
            user_id: Telegram user ID.

        Returns:
            True if favorites were cleared.
            False if user does not exist.
        """
        data = self.load()
        user_key = str(user_id)

        if user_key not in data:
            return False

        data[user_key] = []
        self.save(data)
        return True