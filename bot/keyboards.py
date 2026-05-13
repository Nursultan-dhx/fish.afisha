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