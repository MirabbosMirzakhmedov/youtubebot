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