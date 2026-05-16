import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BotCommand, CallbackQuery, Message

from bot.config import load_config
from bot.keyboards import (
    get_favorites_keyboard,
    get_genres_keyboard,
    get_movie_keyboard,
)
from bot.services.movie_fetcher import MovieFetcher
from bot.storage.favorites_manager import FavoritesManager


dp = Dispatcher()
movie_fetcher = None
favorites_manager = FavoritesManager("data/favorites.json")


async def set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Выбрать жанр фильма"),
        BotCommand(command="favorites", description="Мои избранные фильмы"),
        BotCommand(command="trending", description="Фильм дня"),
        BotCommand(command="weekly", description="Фильм недели"),
    ]

    await bot.set_my_commands(commands)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "👋 Привет! Это Fish Afisha Bot.\n\n"
        "Я помогу тебе найти фильм по жанру.\n"
        "Выбери жанр из списка ниже:\n\n"
        "Доступные команды:\n"
        "/start — выбрать жанр\n"
        "/favorites — избранные фильмы\n"
        "/trending — фильм дня\n"
        "/weekly — фильм недели",
        reply_markup=get_genres_keyboard()
    )


@dp.message(Command("favorites"))
async def favorites_command(message: Message):
    user_favorites = favorites_manager.get_favorites(message.from_user.id)

    if not user_favorites:
        await message.answer(
            "😔 У тебя пока нет избранных фильмов.\n\n"
            "Выбери жанр через /start и нажми ❤️ Add to favorites."
        )
        return

    text = "❤️ <b>Твои избранные фильмы:</b>\n\n"

    for index, movie in enumerate(user_favorites, start=1):
        title = movie.get("title", "Unknown movie")
        year = movie.get("year", "????")
        rating = movie.get("rating", 0)

        text += f"{index}. <b>{title}</b> ({year}) — ⭐ {rating}/10\n"

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_favorites_keyboard(user_favorites)
    )


@dp.message(Command("trending"))
async def trending_command(message: Message):
    if movie_fetcher is None:
        await message.answer(
            "😔 Сервис фильмов временно недоступен. Попробуй позже."
        )
        return

    movie = movie_fetcher.get_trending_movie()

    if not movie:
        await message.answer(
            "😔 Не удалось получить фильм дня.\n"
            "Попробуй позже или выбери жанр через /start."
        )
        return

    formatted_movie = movie_fetcher.format_movie(movie)

    text = (
        f"🔥 <b>Фильм дня</b>\n\n"
        f"🎬 <b>{formatted_movie['title']}</b> ({formatted_movie['year']})\n"
        f"⭐ Рейтинг: {formatted_movie['rating']}/10\n\n"
        f"{formatted_movie['overview']}"
    )

    poster_url = formatted_movie["poster_url"]

    if poster_url:
        await message.answer_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text,
            parse_mode="HTML"
        )


@dp.message(Command("weekly"))
async def weekly_trending_command(message: Message):
    if movie_fetcher is None:
        await message.answer(
            "😔 Сервис фильмов временно недоступен. Попробуй позже."
        )
        return

    movie = movie_fetcher.get_weekly_trending_movie()

    if not movie:
        await message.answer(
            "😔 Не удалось получить фильм недели.\n"
            "Попробуй позже или выбери жанр через /start."
        )
        return

    formatted_movie = movie_fetcher.format_movie(movie)

    text = (
        f"🏆 <b>Фильм недели</b>\n\n"
        f"🎬 <b>{formatted_movie['title']}</b> ({formatted_movie['year']})\n"
        f"⭐ Рейтинг: {formatted_movie['rating']}/10\n\n"
        f"{formatted_movie['overview']}"
    )

    poster_url = formatted_movie["poster_url"]

    if poster_url:
        await message.answer_photo(
            photo=poster_url,
            caption=text,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text,
            parse_mode="HTML"
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


@dp.callback_query(F.data.startswith("remove_favorite_"))
async def remove_favorite(callback: CallbackQuery):
    movie_index = int(callback.data.split("_")[-1])

    removed = favorites_manager.remove_movie_by_index(
        callback.from_user.id,
        movie_index
    )

    if not removed:
        await callback.answer("Не удалось удалить фильм.", show_alert=True)
        return

    user_favorites = favorites_manager.get_favorites(callback.from_user.id)

    if not user_favorites:
        await callback.message.edit_text(
            "😔 Список избранных фильмов пуст."
        )
        await callback.answer("Фильм удален.", show_alert=True)
        return

    text = "❤️ <b>Твои избранные фильмы:</b>\n\n"

    for index, movie in enumerate(user_favorites, start=1):
        title = movie.get("title", "Unknown movie")
        year = movie.get("year", "????")
        rating = movie.get("rating", 0)

        text += f"{index}. <b>{title}</b> ({year}) — ⭐ {rating}/10\n"

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_favorites_keyboard(user_favorites)
    )

    await callback.answer("Фильм удален.", show_alert=True)


@dp.message(F.photo)
async def photo_message_handler(message: Message):
    await message.answer(
        "📸 Я получил изображение.\n\n"
        "Сейчас я подбираю фильмы по жанрам. Используй /start, чтобы выбрать жанр."
    )


@dp.message(F.text)
async def text_message_handler(message: Message):
    await message.answer(
        "💬 Я получил твое сообщение.\n\n"
        "Чтобы начать подбор фильма, используй команду /start.\n"
        "Чтобы посмотреть избранные фильмы, используй /favorites.\n"
        "Чтобы получить фильм дня, используй /trending.\n"
        "Чтобы получить фильм недели, используй /weekly."
    )


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

    await set_bot_commands(bot)

    print("Bot started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())