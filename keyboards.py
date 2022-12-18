from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

language_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text='🇬🇧 English', callback_data='english_welcome_text'
            ),
            InlineKeyboardButton(
                text='🇷🇺 Русский', callback_data='russian_welcome_text'
            )
        ],
    ]
)