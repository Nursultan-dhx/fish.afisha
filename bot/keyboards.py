from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.genres import GENRES


def get_genres_keyboard() -> InlineKeyboardMarkup:
    genre_items = list(GENRES.items())
    rows = []

    for i in range(0, len(genre_items), 2):
        row = []

        for genre_id, genre_name in genre_items[i:i + 2]:
            row.append(
                InlineKeyboardButton(
                    text=genre_name,
                    callback_data=f"genre_{genre_id}"
                )
            )

        rows.append(row)

    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_movie_keyboard(genre_id: str, movie_index: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❤️ В избранное",
                    callback_data=f"like_{genre_id}_{movie_index}"
                ),
                InlineKeyboardButton(
                    text="🔄 Другой фильм",
                    callback_data=f"next_{genre_id}_{movie_index + 1}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎬 Сменить жанр",
                    callback_data="change_genre"
                )
            ]
        ]
    )


def get_favorites_keyboard(favorites: list[dict]) -> InlineKeyboardMarkup:
    rows = []

    for index, movie in enumerate(favorites):
        title = movie.get("title", "Неизвестный фильм")

        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🗑 Удалить {index + 1}. {title[:25]}",
                    callback_data=f"remove_favorite_{index}"
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="🎬 Выбрать жанр",
                callback_data="change_genre"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)