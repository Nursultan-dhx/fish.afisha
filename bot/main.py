import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.config import load_config
from bot.keyboards import get_genres_keyboard, get_movie_keyboard
from bot.services.movie_fetcher import MovieFetcher
from bot.storage.favorites_manager import FavoritesManager


dp = Dispatcher()
movie_fetcher = None
favorites_manager = FavoritesManager("data/favorites.json")


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "👋 Привет! Это Fish Afisha Bot.\n\n"
        "Я помогу тебе найти фильм по жанру.\n"
        "Выбери жанр из списка ниже:",
        reply_markup=get_genres_keyboard()
    )


@dp.callback_query(F.data == "change_genre")
async def change_genre(callback: CallbackQuery):
    await callback.message.answer(
        "🎬 Выбери новый жанр фильма:",
        reply_markup=get_genres_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("genre_"))
async def genre_selected(callback: CallbackQuery):
    genre_id = callback.data.split("_")[1]

    await callback.answer("Ищу фильм...")
    await show_movie(callback, genre_id, 0)


@dp.callback_query(F.data.startswith("next_"))
async def next_movie(callback: CallbackQuery):
    parts = callback.data.split("_")
    genre_id = parts[1]
    movie_index = int(parts[2])

    await callback.answer("Ищу другой фильм...")
    await show_movie(callback, genre_id, movie_index)


@dp.callback_query(F.data.startswith("like_"))
async def like_movie(callback: CallbackQuery):
    parts = callback.data.split("_")
    genre_id = parts[1]
    movie_index = int(parts[2])

    movies = movie_fetcher.get_movies_by_genre(genre_id)

    if not movies:
        await callback.answer("Не удалось добавить фильм.", show_alert=True)
        return

    movie_index = movie_index % len(movies)
    movie = movies[movie_index]
    formatted_movie = movie_fetcher.format_movie(movie)

    movie_data = {
        "title": formatted_movie["title"],
        "year": formatted_movie["year"],
        "rating": formatted_movie["rating"],
        "overview": formatted_movie["overview"],
    }

    added = favorites_manager.add_movie(callback.from_user.id, movie_data)

    if added:
        await callback.answer("❤️ Фильм добавлен в избранное!", show_alert=True)
    else:
        await callback.answer("Этот фильм уже есть в избранном.", show_alert=True)


async def show_movie(callback: CallbackQuery, genre_id: str, movie_index: int):
    movies = movie_fetcher.get_movies_by_genre(genre_id)

    if not movies:
        await callback.message.answer(
            "😔 Не удалось найти фильмы по этому жанру.\n"
            "Попробуй выбрать другой жанр."
        )
        return

    movie_index = movie_index % len(movies)
    movie = movies[movie_index]
    formatted_movie = movie_fetcher.format_movie(movie)

    text = (
        f"🎬 <b>{formatted_movie['title']}</b> ({formatted_movie['year']})\n"
        f"⭐ Рейтинг: {formatted_movie['rating']}/10\n\n"
        f"{formatted_movie['overview']}"
    )

    keyboard = get_movie_keyboard(genre_id, movie_index)
    poster_url = formatted_movie["poster_url"]

    if poster_url:
        await callback.message.answer_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await callback.message.answer(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
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