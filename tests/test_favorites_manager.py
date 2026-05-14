from bot.storage.favorites_manager import FavoritesManager


def test_get_favorites_returns_empty_list_for_new_user(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    result = manager.get_favorites(user_id=1)

    assert result == []


def test_add_movie_saves_movie_to_favorites(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "title": "Inception",
        "year": "2010",
        "rating": 8.8,
        "overview": "A thief enters people's dreams."
    }

    added = manager.add_movie(user_id=1, movie=movie)
    favorites = manager.get_favorites(user_id=1)

    assert added is True
    assert len(favorites) == 1
    assert favorites[0]["title"] == "Inception"


def test_add_movie_does_not_add_duplicate(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "title": "Interstellar",
        "year": "2014",
        "rating": 8.7,
        "overview": "A space exploration movie."
    }

    first_add = manager.add_movie(user_id=1, movie=movie)
    second_add = manager.add_movie(user_id=1, movie=movie)
    favorites = manager.get_favorites(user_id=1)

    assert first_add is True
    assert second_add is False
    assert len(favorites) == 1


def test_movie_exists_returns_true_for_existing_movie(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "title": "The Matrix",
        "year": "1999",
        "rating": 8.7,
        "overview": "A hacker discovers the truth about reality."
    }

    manager.add_movie(user_id=1, movie=movie)

    assert manager.movie_exists(user_id=1, title="The Matrix") is True


def test_movie_exists_returns_false_for_missing_movie(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    assert manager.movie_exists(user_id=1, title="Avatar") is False


def test_remove_movie_by_index_removes_correct_movie(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    first_movie = {
        "title": "Movie One",
        "year": "2020",
        "rating": 7.0,
        "overview": "First movie."
    }

    second_movie = {
        "title": "Movie Two",
        "year": "2021",
        "rating": 8.0,
        "overview": "Second movie."
    }

    manager.add_movie(user_id=1, movie=first_movie)
    manager.add_movie(user_id=1, movie=second_movie)

    removed = manager.remove_movie_by_index(user_id=1, movie_index=0)
    favorites = manager.get_favorites(user_id=1)

    assert removed is True
    assert len(favorites) == 1
    assert favorites[0]["title"] == "Movie Two"


def test_remove_movie_by_index_returns_false_for_invalid_index(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "title": "Tenet",
        "year": "2020",
        "rating": 7.3,
        "overview": "Time inversion thriller."
    }

    manager.add_movie(user_id=1, movie=movie)

    removed = manager.remove_movie_by_index(user_id=1, movie_index=5)
    favorites = manager.get_favorites(user_id=1)

    assert removed is False
    assert len(favorites) == 1


def test_clear_favorites_removes_all_user_movies(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "title": "Dune",
        "year": "2021",
        "rating": 8.0,
        "overview": "A science fiction movie."
    }

    manager.add_movie(user_id=1, movie=movie)

    cleared = manager.clear_favorites(user_id=1)
    favorites = manager.get_favorites(user_id=1)

    assert cleared is True
    assert favorites == []


def test_add_movie_without_title_returns_false(tmp_path):
    file_path = tmp_path / "favorites.json"
    manager = FavoritesManager(str(file_path))

    movie = {
        "year": "2022",
        "rating": 6.5,
        "overview": "Movie without title."
    }

    added = manager.add_movie(user_id=1, movie=movie)
    favorites = manager.get_favorites(user_id=1)

    assert added is False
    assert favorites == []