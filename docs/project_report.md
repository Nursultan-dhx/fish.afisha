# Project Report: Fish Afisha Bot

## 1. Problem Statement

Many users spend a lot of time choosing what movie to watch. They may not know which movie is popular now, which movie fits their preferred genre, or how to save interesting movies for later. The goal of this project is to create a Telegram bot that helps users quickly find movie recommendations, view trending movies, and manage a personal list of favorite movies.

Fish Afisha Bot solves this problem by providing a simple Telegram interface where users can choose a movie genre, receive recommendations from the TMDB API, view daily and weekly trending movies, and save selected movies to a local JSON file.

## 2. Solution Overview

Fish Afisha Bot is a Telegram bot built with Python and aiogram. The bot interacts with users through commands and inline keyboards. Users can select genres, receive movie recommendations, add movies to favorites, view saved movies, and remove movies from favorites.

The project uses the TMDB API to get real movie information, including movie titles, descriptions, ratings, release years, and posters. Favorite movies are stored locally in a JSON file, which demonstrates data persistence.

Main bot commands:

- `/start` — opens the genre selection menu.
- `/favorites` — shows the user's saved favorite movies.
- `/trending` — shows the trending movie of the day.
- `/weekly` — shows the trending movie of the week.

The bot also handles regular text messages and image messages, so it supports different message types required for a Telegram bot project.

## 3. Simple System Design

The project is divided into several modules to keep the code clean and organized.

```text
fish.afisha/
│
├── bot/
│   ├── config.py
│   ├── genres.py
│   ├── keyboards.py
│   ├── main.py
│   │
│   ├── services/
│   │   └── movie_fetcher.py
│   │
│   └── storage/
│       └── favorites_manager.py
│
├── data/
│   └── favorites.example.json
│
├── tests/
│   └── test_favorites_manager.py
│
├── README.md
├── requirements.txt
└── .env.example
```

### Main Components

### Telegram Bot Layer

The file `bot/main.py` contains the main Telegram bot logic:

- command handlers;
- callback handlers;
- text message handling;
- photo message handling;
- integration between user actions and backend services.

### Keyboard Layer

The file `bot/keyboards.py` contains inline keyboard generation:

- genre selection keyboard;
- movie action buttons;
- favorites removal buttons.

### API Layer

The file `bot/services/movie_fetcher.py` contains the `MovieFetcher` class. This class is responsible for:

- fetching movies by genre from TMDB;
- fetching daily trending movies;
- fetching weekly trending movies;
- formatting movie data;
- handling API errors.

### Storage Layer

The file `bot/storage/favorites_manager.py` contains the storage classes:

- `StorageManager` — base class for JSON file operations;
- `FavoritesManager` — child class for favorite movie operations.

This demonstrates inheritance, which is an advanced OOP concept.

### Testing Layer

The `tests/` folder contains unit tests for the favorites manager. The tests check adding movies, preventing duplicates, removing movies, clearing favorites, and handling invalid data.

## 4. Object-Oriented Programming

The project uses classes and objects to organize the logic.

### MovieFetcher

`MovieFetcher` handles all TMDB API operations. It keeps API logic separate from Telegram handlers.

### StorageManager

`StorageManager` is a base class that provides common JSON file operations such as loading and saving data.

### FavoritesManager

`FavoritesManager` inherits from `StorageManager`. It manages user favorite movies and provides methods for:

- adding movies;
- checking duplicates;
- getting favorite movies;
- removing movies by index;
- clearing favorites.

This inheritance structure demonstrates an advanced OOP concept.

## 5. Data Persistence

The project uses JSON file storage for favorite movies. Runtime data is stored in:

```text
data/favorites.json
```

This file is ignored by Git because it can contain real Telegram user IDs and test data.

The repository includes an example file:

```text
data/favorites.example.json
```

The bot can read from and write to JSON, which satisfies the data persistence requirement.

## 6. Robustness and Error Handling

The project includes exception handling to prevent crashes.

Examples of handled situations:

- missing environment variables;
- failed TMDB API requests;
- invalid TMDB API responses;
- missing JSON storage file;
- invalid JSON content;
- invalid favorite movie indexes;
- empty favorite lists;
- missing movie data.

If an error happens, the bot returns a user-friendly message instead of crashing.

## 7. Challenges Faced

During the project development, the team faced several challenges:

1. **Git and GitHub workflow**  
   The team needed to create a clean commit history and show the contribution of both members.

2. **Environment variables**  
   Bot tokens and API keys had to be moved to `.env` to avoid exposing sensitive data in GitHub.

3. **JSON storage management**  
   The team had to separate real runtime data from example data and ignore `favorites.json` in Git.

4. **Telegram callback handling**  
   The bot needed to correctly process different callback buttons, including genre selection, next movie, adding to favorites, and removing from favorites.

5. **API error handling**  
   TMDB API requests needed exception handling to avoid crashes if the API was unavailable or returned unexpected data.

6. **Project structure**  
   The project was divided into modules to improve readability and maintainability.

## 8. Team Contributions

### Nursultan

Nursultan was responsible for the Telegram bot interface and user interaction.

Main contributions:

- initial bot setup;
- command handlers;
- callback handlers;
- inline keyboards;
- genre selection interface;
- movie recommendation flow;
- favorite movie buttons;
- `/favorites` command;
- `/trending` command;
- `/weekly` command;
- text and photo message handlers;
- bot command menu;
- user message improvements;
- README documentation.

### Dastan

Dastan was responsible for backend logic, API integration, storage, OOP structure, and testing.

Main contributions:

- movie genre data structure;
- TMDB API integration;
- `MovieFetcher` class;
- daily trending movie fetcher;
- weekly trending movie fetcher;
- API error handling;
- JSON storage logic;
- `StorageManager` and `FavoritesManager` classes;
- inheritance-based OOP structure;
- remove favorite storage logic;
- unit tests for favorites manager;
- API and storage module documentation.

## 9. Testing

The project uses `pytest` for unit testing.

The tests are located in:

```text
tests/test_favorites_manager.py
```

The tests check:

- getting empty favorites;
- adding movies;
- preventing duplicate movies;
- checking if a movie exists;
- removing movies by index;
- handling invalid indexes;
- clearing favorites;
- rejecting movies without a title.

To run tests:

```bash
python -m pytest
```

Expected result:

```text
9 passed
```

## 10. Conclusion

Fish Afisha Bot is a functional Telegram bot that helps users find movies by genre, view trending movies, and save favorite movies. The project uses Python, aiogram, TMDB API, JSON storage, OOP, exception handling, modular code structure, and unit tests.

The project meets the main technical requirements for the final project and demonstrates teamwork through a clear division of responsibilities and a structured Git commit history.
