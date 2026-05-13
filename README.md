# Fish Afisha Bot

Fish Afisha Bot is a Telegram bot that will help users find movie recommendations by genre.

## Current Status

Initial project setup.

At this stage, the bot only supports the `/start` command and basic configuration loading.
More features will be added step by step in future commits.

## Planned Features

- Genre selection menu
- Movie recommendations using TMDB API
- Favorite movies list
- JSON data storage
- Error handling
- Modular project structure

## Technologies

- Python
- aiogram
- TMDB API
- JSON

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Nursultan-dhx/fish.afisha.git
cd fish.afisha
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the bot from the project root folder:

```bash
python -m bot.main
```

## Team Roles

- Nursultan: Telegram bot setup, commands, handlers, user interaction
- Dastan: TMDB API logic, JSON storage, OOP structure, error handling