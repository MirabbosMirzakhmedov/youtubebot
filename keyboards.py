from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text='Video 🎬', callback_data='video_callback_data'
            ),
            InlineKeyboardButton(
                text='Audio 🎵', callback_data='audio_callback_data'
            )
        ],
        [
            InlineKeyboardButton(
                text='Playlist video 🎞', callback_data='playlist_video_callback_data'
            ),
            InlineKeyboardButton(
                text='Playlist audio 🎶', callback_data='playlist_audio_callback_data'
            )
        ],
        [
            InlineKeyboardButton(
                text='Thumbnail photo 🎆', callback_data='thumbnail_callback_data'
            )
        ]
    ]
)

support_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text='Support Us ❤️', callback_data='support_button'
            )
        ]
    ]
)

support_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text='PayPal 💳', callback_data='paypal_button'
            ),
            InlineKeyboardButton(
                text='Contacts 👨🏻‍💻', callback_data='contact_button'
            )
        ],
        [
            InlineKeyboardButton(
                text='◀ Home', callback_data='back_to_main'
            )
        ]
    ]
)

back_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text='◀ Back', callback_data='back_button'
            )
        ]
    ]
)