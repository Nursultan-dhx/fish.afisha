import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.config import load_config
from bot.keyboards import get_genres_keyboard
from bot.services.movie_fetcher import MovieFetcher


dp = Dispatcher()
movie_fetcher = None


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

    await callback.answer("Ищу фильм...")

    movies = movie_fetcher.get_movies_by_genre(genre_id)

    if not movies:
        await callback.message.answer(
            "😔 Не удалось найти фильмы по этому жанру.\n"
            "Попробуй выбрать другой жанр."
        )
        return

    movie = movies[0]
    formatted_movie = movie_fetcher.format_movie(movie)

    text = (
        f"🎬 <b>{formatted_movie['title']}</b> ({formatted_movie['year']})\n"
        f"⭐ Рейтинг: {formatted_movie['rating']}/10\n\n"
        f"{formatted_movie['overview']}"
    )

    poster_url = formatted_movie["poster_url"]

    if poster_url:
        await callback.message.answer_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            text,
            parse_mode="HTML"
        )


async def main():
    global movie_fetcher

    config = load_config()

    bot = Bot(token=config["BOT_TOKEN"])
    movie_fetcher = MovieFetcher(config["TMDB_API_KEY"])

    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())