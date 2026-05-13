import os
from dotenv import load_dotenv


def load_config():
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    tmdb_api_key = os.getenv("TMDB_API_KEY")

    if not bot_token:
        raise ValueError("BOT_TOKEN is missing in .env file")

    if not tmdb_api_key:
        raise ValueError("TMDB_API_KEY is missing in .env file")

    return {
        "BOT_TOKEN": bot_token,
        "TMDB_API_KEY": tmdb_api_key,
    }