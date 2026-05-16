# Project Report: Fish Afisha Bot

## 1. Problem Statement

Many users spend too much time choosing what movie to watch. They may not know which movie is popular, which movie fits their preferred genre, or how to save interesting movies for later. The goal of Fish Afisha Bot is to help users quickly find movie recommendations directly inside Telegram.

## 2. Solution Overview

Fish Afisha Bot is a Telegram bot built with Python and aiogram. The bot uses the TMDB API to get real movie data, including titles, descriptions, ratings, release years, posters, and trending movies.

Users can choose a movie genre, receive recommendations, view the movie of the day and movie of the week, add movies to favorites, view saved favorites, and remove movies from the list. Favorite movies are stored locally in a JSON file.

Main commands:

- `/start` — opens the genre selection menu.
- `/favorites` — shows saved favorite movies.
- `/trending` — shows the daily trending movie.
- `/weekly` — shows the weekly trending movie.

The bot also handles regular text messages and image messages, which satisfies the requirement for handling different Telegram message types.

## 3. System Design

The project is divided into modules to keep the code clean and maintainable.

```text
fish.afisha/
├── bot/
│   ├── config.py
│   ├── genres.py
│   ├── keyboards.py
│   ├── main.py
│   ├── services/movie_fetcher.py
│   └── storage/favorites_manager.py
├── data/favorites.example.json
├── tests/test_favorites_manager.py
├── README.md
└── requirements.txt
```

Main components:

- `bot/main.py` — Telegram commands, message handlers, callback handlers, and bot startup.
- `bot/keyboards.py` — inline keyboards for genres, movie actions, and favorites.
- `bot/services/movie_fetcher.py` — TMDB API logic and movie formatting.
- `bot/storage/favorites_manager.py` — JSON storage logic for favorite movies.
- `tests/test_favorites_manager.py` — unit tests for storage functionality.

## 4. OOP, Data Persistence, and Error Handling

The project uses object-oriented programming to separate responsibilities:

- `MovieFetcher` handles TMDB API requests, daily and weekly trending movies, movie filtering, and movie formatting.
- `StorageManager` is a base class for JSON file operations.
- `FavoritesManager` inherits from `StorageManager` and manages users' favorite movies.

The inheritance between `StorageManager` and `FavoritesManager` demonstrates an advanced OOP concept.

Data persistence is implemented through JSON. Runtime favorite movies are stored in `data/favorites.json`, while GitHub stores only `data/favorites.example.json` to avoid committing real Telegram user IDs.

The project includes exception handling for missing environment variables, failed API requests, invalid API responses, missing or invalid JSON files, storage save errors, and invalid favorite indexes. This prevents the bot from crashing during normal usage and live demonstration.

## 5. Testing

The project uses `pytest` for unit testing. The tests verify that the favorites storage manager can:

- return an empty list for a new user;
- add movies to favorites;
- prevent duplicate movies;
- check if a movie exists;
- remove movies by index;
- reject invalid indexes;
- clear favorites;
- reject movies without a title.

The current test result is:

```text
9 passed
```

## 6. Challenges Faced

The team faced several challenges during development:

1. Creating a clean GitHub commit history that shows contributions from both members.
2. Moving bot tokens and API keys to `.env` to avoid exposing secrets.
3. Separating real runtime data from example JSON files.
4. Handling Telegram callback buttons for genre selection, movie actions, favorites, and removal.
5. Adding error handling for TMDB API requests and JSON storage.
6. Keeping the project modular and easy to explain during defense.

## 7. Team Contributions

### Nursultan

Nursultan was responsible for the Telegram bot interface and user interaction:

- initial bot setup;
- command handlers;
- callback handlers;
- inline keyboards;
- genre selection interface;
- movie recommendation flow;
- favorite movie buttons;
- `/favorites`, `/trending`, and `/weekly` commands;
- text and photo message handlers;
- bot command menu;
- user message improvements;
- README documentation.

### Dastan

Dastan was responsible for backend logic, API integration, storage, OOP structure, and testing:

- movie genre data structure;
- TMDB API integration;
- `MovieFetcher` class;
- daily and weekly trending movie fetchers;
- API error handling;
- JSON storage logic;
- `StorageManager` and `FavoritesManager` classes;
- inheritance-based OOP structure;
- remove favorite storage logic;
- unit tests for favorites manager;
- API and storage module documentation.

## 8. Conclusion

Fish Afisha Bot is a functional Telegram bot that helps users find movies by genre, view trending movies, and save favorite movies. The project uses Python, aiogram, TMDB API, JSON storage, OOP, exception handling, modular structure, and unit tests.

The project meets the main final project requirements and demonstrates teamwork through clear role division and a structured Git commit history.
