import os
from dotenv import load_dotenv


def load_config() -> dict:
    """Load application configuration from environment variables."""
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise ValueError("BOT_TOKEN is missing. Please add it to your .env file.")

    return {
        "BOT_TOKEN": bot_token,
        "TMDB_API_KEY": os.getenv("TMDB_API_KEY", ""),
    }
