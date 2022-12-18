# Importing packages, modules and libraries
import os.path

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, ForceReply, Message
from pythumb import Thumbnail
from pytube import YouTube, Playlist

from data import error_message, bot_message, welcome_text, client_reply
from keyboards import language_keyboard
from secret import API_ID, API_HASH, BOT_TOKEN, ID

# registering the bot
bot = Client(
    "YoutubeDownloader",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Function to reply /start command
@bot.on_message(filters.command(commands=['start']) & filters.private)
async def welcome(client: Client, message: Message):
    await message.reply_text(
        text=f"Hello, {message.from_user.first_name}!\n\n" +
             welcome_text['english'],
        disable_web_page_preview=False,
        reply_markup=language_keyboard
    )


# Function that sends different language texts
@bot.on_callback_query(filters.regex('welcome_text'))
async def language_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'russian_welcome_text':
        try:
            await update.edit_message_text(
                text=f"Здравствуйте, {update.message.chat.first_name}!\n\n" +
                     welcome_text['russian'],
                reply_markup=language_keyboard,
                disable_web_page_preview=True
            )
        except Exception:
            pass
    else:
        try:
            await update.edit_message_text(
                text=f"Hello, {update.message.chat.first_name}!\n\n" +
                     welcome_text['english'],
                reply_markup=language_keyboard,
                disable_web_page_preview=True
            )
        except Exception:
            pass


# Function to reply /video command
@bot.on_message(filters.command(commands=['video']) & filters.private)
async def get_video(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=client_reply,
        reply_markup=ForceReply(placeholder='High quality video')
    )


# Function to reply /audio command
@bot.on_message(filters.command(commands=['audio']) & filters.private)
async def get_audio(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=client_reply,
        reply_markup=ForceReply(placeholder='Audio only'),
        disable_web_page_preview=True
    )


# Function to reply /playlist_videos command
@bot.on_message(
    filters.command(commands=['playlist_videos']) & filters.private)
async def get_playlist_video(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=client_reply,
        reply_markup=ForceReply(placeholder='Playlist videos'),
        disable_web_page_preview=True
    )


# Function to reply /playlist_audios command
@bot.on_message(
    filters.command(commands=['playlist_audios']) & filters.private)
async def get_playlist_audios(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=client_reply,
        reply_markup=ForceReply(placeholder='Playlist audios'),
        disable_web_page_preview=True
    )


# Function to reply /thumbnail command
@bot.on_message(filters.command(commands=['thumbnail']) & filters.private)
async def get_thumbnail(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=client_reply,
        reply_markup=ForceReply(placeholder='Thumbnail photo'),
        disable_web_page_preview=True
    )


# main downloader function
@bot.on_message(filters.private)
async def download(client: Client, update: Message) -> None:
    if update.reply_to_message:
        if update.reply_to_message.reply_markup.placeholder == "High quality video":
            processing = await client.send_message(
                update.chat.id,
                'Processing your request...',
                reply_to_message_id=update.id
            )
            try:
                video = YouTube(update.text)
                caption = f"**{video.title}**\n\n" \
                          f"Channel - **[{video.author}]({video.channel_url})**"
                video = video.streams.get_highest_resolution()
                try:
                    await client.edit_message_text(
                        chat_id=update.chat.id,
                        text="Success! We'll send it in a second!",
                        message_id=processing.id
                    )
                    high_res_video = video.download()
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_document(chat_id=update.chat.id,
                                               document=high_res_video,
                                               caption=caption)
                    if os.path.exists(high_res_video):
                        os.remove(high_res_video)
                    await client.send_message(
                        update.chat.id,
                        'All done, finished.',
                    )
                except Exception as err:
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_message(chat_id=ID,
                                              text=f'There has been an error:\n\n{err}')

            except Exception:
                await client.delete_messages(chat_id=update.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=update.chat.id,
                                          text=error_message)

        elif update.reply_to_message.reply_markup.placeholder == "Audio only":
            processing = await client.send_message(
                update.chat.id,
                'Processing your request...',
                reply_to_message_id=update.id
            )
            try:
                audio = YouTube(update.text)
                caption = f"**{audio.title}**\n\n" \
                          f"Channel - **[{audio.author}]({audio.channel_url})**"
                audio = audio.streams.get_audio_only()
                try:
                    await client.edit_message_text(
                        chat_id=update.chat.id,
                        text="Success! We'll send it in a second!",
                        message_id=processing.id
                    )
                    out_file = audio.download()
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + ".mp3"
                    os.rename(out_file, new_file)
                    await client.send_audio(chat_id=update.chat.id,
                                            audio=new_file,
                                            caption=caption)
                    if os.path.exists(new_file):
                        os.remove(new_file)
                    await client.send_message(
                        update.chat.id,
                        'All done, finished.',
                    )
                except Exception as err:
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_message(chat_id=ID,
                                              text=f'There has been an error:\n\n{err}')
            except Exception:
                await client.delete_messages(chat_id=update.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=update.chat.id,
                                          text=error_message)

        elif update.reply_to_message.reply_markup.placeholder == "Playlist videos":
            processing = await client.send_message(
                update.chat.id,
                'Processing your request...',
                reply_to_message_id=update.id
            )
            try:
                playlist = Playlist(update.text)
                try:
                    for playlist_video in playlist.videos:
                        video = playlist_video.streams.get_highest_resolution()
                        downloaded_video = video.download()
                        await client.delete_messages(chat_id=update.chat.id,
                                                     message_ids=processing.id)
                        await client.send_document(chat_id=update.chat.id,
                                                   document=downloaded_video,
                                                   caption=f"**{playlist_video.title}**\n\n" \
                                                           f"Playlist - **[{playlist.title}]({playlist.playlist_url})**\n"
                                                           f"Channel - **[{playlist_video.author}]({playlist_video.channel_url})**"
                                                   )
                        if os.path.exists(downloaded_video):
                            os.remove(downloaded_video)
                    await client.send_message(chat_id=update.chat.id,
                                              text='All done, finished.')
                except Exception:
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_message(chat_id=update.chat.id,
                                              text=error_message)
            except Exception as err:
                await client.delete_messages(chat_id=update.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=ID,
                                          text=f'There has been an error:\n\n{err}')

        elif update.reply_to_message.reply_markup.placeholder == "Playlist audios":
            processing = await client.send_message(
                update.chat.id,
                'Processing your request...',
                reply_to_message_id=update.id
            )
            try:
                playlist = Playlist(update.text)
                try:
                    for playlist_video in playlist.videos:
                        audio = playlist_video.streams.get_audio_only()
                        out_file = audio.download()
                        await client.delete_messages(chat_id=update.chat.id,
                                                     message_ids=processing.id)
                        base, ext = os.path.splitext(out_file)
                        new_file = base + ".mp3"
                        os.rename(out_file, new_file)

                        await client.send_audio(chat_id=update.chat.id,
                                                audio=new_file,
                                                caption=f"**{playlist_video.title}**\n\n" \
                                                        f"Playlist - **[{playlist.title}]({playlist.playlist_url})**\n"
                                                        f"Channel - **[{playlist_video.author}]({playlist_video.channel_url})**")

                        if os.path.exists(new_file):
                            os.remove(new_file)
                    await client.send_message(chat_id=update.chat.id,
                                              text='All done, finished.')
                except Exception:
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_message(chat_id=update.chat.id,
                                              text=error_message)
            except Exception as err:
                await client.delete_messages(chat_id=update.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=ID,
                                          text=f'There has been an error:\n\n{err}')

        elif update.reply_to_message.reply_markup.placeholder == "Thumbnail photo":
            processing = await client.send_message(
                update.chat.id,
                'Processing your request...',
                reply_to_message_id=update.id
            )
            try:
                video = YouTube(update.text)
                photo = Thumbnail(update.text)
                caption = f"**{video.title}**\n\n" \
                          f"Channel - **[{video.author}]({video.channel_url})**"
                try:
                    photo.fetch()
                    ready_photo = photo.save('.')
                    await client.edit_message_text(
                        chat_id=update.chat.id,
                        text="Success! We'll send it in a second!",
                        message_id=processing.id
                    )
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_photo(chat_id=update.chat.id,
                                            photo=ready_photo,
                                            caption=caption)
                    if os.path.exists(ready_photo):
                        os.remove(ready_photo)
                    await client.send_message(
                        update.chat.id,
                        'All done, finished.',
                    )
                except Exception as err:
                    await client.delete_messages(chat_id=update.chat.id,
                                                 message_ids=processing.id)
                    await client.send_message(chat_id=ID,
                                              text=f'There has been an error:\n\n{err}')
            except Exception:
                await client.delete_messages(chat_id=update.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=update.chat.id,
                                          text=error_message)
    else:
        await client.send_message(
            text=bot_message,
            chat_id=update.chat.id,
        )


print('Youtube Downloader has started')
if __name__ == "__main__":
    bot.run()
