import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import load_config


dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message) -> None:
    """Handle the /start command."""
    await message.answer(
        "👋 Привет! Это Fish Afisha Bot.\n\n"
        "Скоро я буду помогать тебе находить фильмы по жанрам 🎬"
    )


async def main() -> None:
    """Start the Telegram bot."""
    config = load_config()
    bot = Bot(token=config["BOT_TOKEN"])

    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
