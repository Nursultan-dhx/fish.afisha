# Fish Afisha Bot

Fish Afisha Bot is a Telegram bot that helps users find movie recommendations by genre, view trending movies, and save favorite movies.

The bot uses the TMDB API to get real movie data and stores users' favorite movies locally in a JSON file.

---

## Project Type

Telegram Bot

---

## Features

- Choose movie genres using inline buttons
- Get movie recommendations by genre
- View the daily trending movie
- View the weekly trending movie
- Add movies to favorites
- View saved favorite movies
- Remove movies from favorites
- Handle commands, text messages, callback buttons, and images
- Store user favorites in a JSON file
- Use OOP classes for API and storage logic
- Handle API and file errors safely
- Unit tests for favorites storage logic

---

## Technologies Used

- Python
- aiogram
- TMDB API
- JSON
- requests
- python-dotenv
- pytest
- Git / GitHub

---

## Project Structure

```text
fish.afisha/
|
├── bot/
│   ├── __init__.py
│   ├── config.py
│   ├── genres.py
│   ├── keyboards.py
│   ├── main.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── movie_fetcher.py
│   │
│   └── storage/
│       ├── __init__.py
│       └── favorites_manager.py
│
├── data/
│   └── favorites.example.json
│
├── tests/
│   ├── __init__.py
│   └── test_favorites_manager.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Team Roles

### Nursultan

Responsible for Telegram bot interface and user interaction:

- Initial bot setup
- Telegram commands
- Message handlers
- Callback handlers
- Inline keyboards
- Genre selection interface
- Favorite movie buttons
- `/favorites` command
- `/trending` command
- `/weekly` command
- Text and image message handlers
- User-friendly bot messages

### Dastan

Responsible for backend logic, API, storage, and testing:

- Movie genre data structure
- TMDB API integration
- MovieFetcher class
- Daily trending movie fetcher
- Weekly trending movie fetcher
- JSON favorites storage
- OOP storage structure
- FavoritesManager class
- Remove favorite logic
- Error handling
- Unit tests for favorites manager
- API and storage documentation

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nursultan-dhx/fish.afisha.git
cd fish.afisha
```

### 2. Create virtual environment

For Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

For macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root folder of the project.

Example:

```env
BOT_TOKEN=your_telegram_bot_token_here
TMDB_API_KEY=your_tmdb_api_key_here
```

The `.env` file is ignored by Git for security reasons.

Use `.env.example` as a template.

---

## How to Run the Bot

Run the project from the root folder:

```bash
python -m bot.main
```

If the bot starts successfully, you will see:

```text
Bot started...
```

---

## Bot Commands

| Command | Description |
|---|---|
| `/start` | Opens the genre selection menu |
| `/favorites` | Shows user's saved favorite movies |
| `/trending` | Shows the daily trending movie |
| `/weekly` | Shows the weekly trending movie |

---

## How to Use

1. Start the bot with `/start`.
2. Choose a movie genre using inline buttons.
3. The bot sends a movie recommendation from TMDB.
4. Press `❤️ В избранное` to save the movie.
5. Press `🔄 Другой фильм` to get another recommendation.
6. Press `🎬 Сменить жанр` to choose another genre.
7. Use `/favorites` to view saved movies.
8. Remove saved movies using the delete buttons.
9. Use `/trending` to get the movie of the day.
10. Use `/weekly` to get the movie of the week.

---

## Data Persistence

The project uses JSON file storage for favorite movies.

Runtime data is stored in:

```text
data/favorites.json
```

This file is ignored by Git because it can contain real Telegram user IDs and test data.

The repository includes an example file:

```text
data/favorites.example.json
```

Example content:

```json
{}
```

---

## Object-Oriented Programming

The project uses OOP classes:

### MovieFetcher

Located in:

```text
bot/services/movie_fetcher.py
```

Responsible for:

- fetching movies by genre;
- fetching daily trending movie;
- fetching weekly trending movie;
- formatting movie data;
- handling TMDB API errors.

### StorageManager

Located in:

```text
bot/storage/favorites_manager.py
```

Base class for JSON file operations:

- creating storage file;
- loading JSON data;
- saving JSON data;
- handling JSON/file errors.

### FavoritesManager

Located in:

```text
bot/storage/favorites_manager.py
```

Inherits from `StorageManager`.

Responsible for:

- adding movies to favorites;
- checking duplicates;
- getting user favorites;
- removing movies by index;
- clearing favorites.

This inheritance demonstrates an advanced OOP concept.

---

## Error Handling

The project includes exception handling for:

- failed TMDB API requests;
- invalid TMDB API responses;
- missing JSON file;
- invalid JSON file;
- storage save errors;
- invalid favorite movie indexes;
- missing environment variables.

This helps prevent crashes during live demo and normal usage.

---

## Running Tests

The project uses `pytest`.

Run tests with:

```bash
python -m pytest
```

Expected result:

```text
9 passed
```

Current tests check:

- getting empty favorites;
- adding movies;
- preventing duplicates;
- checking existing movies;
- removing movies by index;
- handling invalid indexes;
- clearing favorites;
- rejecting movies without a title.

---

## GitHub Workflow

The project was developed gradually using Git commits from both team members.

The commit history shows division of work:

- Nursultan worked on Telegram bot setup, commands, handlers, keyboards, and user interaction.
- Dastan worked on TMDB API logic, JSON storage, OOP structure, error handling, and tests.

---

## Security Notes

Sensitive data is not stored in the repository.

The following file is ignored by Git:

```text
.env
```

The bot token and TMDB API key must be stored only in the local `.env` file.

---

## Future Improvements

Possible improvements:

- Search movies by title
- Add movie details page
- Add movie trailers
- Add pagination for favorites
- Add user language selection
- Deploy the bot to a cloud server

---

## Authors

- Nursultan
- Dastan
