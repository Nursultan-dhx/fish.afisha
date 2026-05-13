import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.config import load_config
from bot.keyboards import get_genres_keyboard


dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "👋 Привет! Это Fish Afisha Bot.\n\n"
        "Я помогу тебе найти фильм по жанру.\n"
        "Выбери жанр из списка ниже:",
        reply_markup=get_genres_keyboard()
    )


@dp.callback_query(F.data.startswith("genre_"))
async def genre_selected(callback: CallbackQuery):
    genre_id = callback.data.split("_")[1]

    await callback.message.answer(
        f"🎬 Ты выбрал жанр с ID: {genre_id}.\n\n"
        "В следующем обновлении мы подключим рекомендации фильмов через TMDB API."
    )

    await callback.answer()


async def main():
    config = load_config()
    bot = Bot(token=config["BOT_TOKEN"])

    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())