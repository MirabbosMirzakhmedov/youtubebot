# Importing dependencies
import os.path
import sqlite3

import validators
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message, ForceReply
from pythumb import Thumbnail
from pytube import YouTube, Playlist

from data import messages
from keyboards import main_keyboard
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
    text = f"Command: **/start**\n" \
           f"First Name: **{message.from_user.first_name}**\n" \
           f"Username: **@{message.from_user.username}**\n" \
           f"Date: **{message.date.strftime('%d/%b/%Y %H:%M %p')}**\n" \
           f"Chat ID: **{message.from_user.id}**\n\n"
    await message.forward(ID, message.text)
    await client.send_message(text=text, chat_id=ID)
    await message.reply_text(
        text=f"Hello, {message.from_user.first_name}!\n\n" +
             messages['welcome_text'],
        disable_web_page_preview=False,
    )


@bot.on_message(filters.command(["postman"]) & filters.private)
async def get_search_query(client: Client, update: Message) -> None:
    if update.chat.id == ID:
        await update.reply_text(
            text="Please send your message and I will forward it to all users.",
            reply_markup=ForceReply(
                placeholder="Postman"
            )
        )


@bot.on_message(filters.command(["message_to"]) & filters.private)
async def get_search_query(client: Client, update: Message) -> None:
    if update.chat.id == ID:
        await update.reply_text(
            text="Please send your message and I will forward it to one user",
            reply_markup=ForceReply(
                placeholder="Message to"
            )
        )


@bot.on_message(filters.private)
async def download(client: Client, update: Message) -> None:
    if update.reply_to_message:
        if update.reply_to_message.reply_markup.placeholder == "Postman":
            connection = sqlite3.connect("YoutubeDownloader.session")
            crsr = connection.cursor()
            crsr.execute("SELECT id FROM peers;")
            users_ids = crsr.fetchall()

            for user_id in users_ids:
                id = int(user_id[0])
                try:
                    await client.send_message(
                        chat_id=id,
                        text=update.text
                    )
                except:
                    pass

            await client.send_message(
                ID,
                text='The message is sent to all users.'
            )

        if update.reply_to_message:
            if update.reply_to_message.reply_markup.placeholder == "Message to":
                chat_id, text = update.text.split('\n', 1)
                try:
                    await client.send_message(
                        chat_id=chat_id,
                        text=text
                    )
                    await client.send_message(
                        chat_id=ID,
                        text=f'Message is sent.'
                    )
                except Exception as err:
                    await client.send_message(
                        chat_id=ID,
                        text=f'Message was not sent.\n\n{err}'
                    )

    await update.forward(ID, update.text)
    await client.send_message(chat_id=ID, text=f'Chat id: `{update.chat.id}`')

    if validators.url(update.text):
        await client.send_message(
            text=f"**What do you want to download?**\n\n{update.text}",
            chat_id=update.chat.id,
            reply_markup=main_keyboard
        )
    else:
        await client.send_message(
            text=messages['error_message'],
            chat_id=update.chat.id
        )


@bot.on_callback_query(filters.regex(""))
async def income_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'video_callback_data':
        processing = await client.edit_message_text(
            text=messages['process_message'],
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        try:
            link = update.message.text
            video = YouTube(link.split("\n\n", 1)[1])
            caption = f"**{video.title}**\n\n" \
                      f"Channel - **[{video.author}]({video.channel_url})**"
            video = video.streams.get_highest_resolution()

            try:
                if video.filesize >= 2097152000:
                    await client.edit_message_text(
                        text=messages['filesize_error'],
                        chat_id=update.message.chat.id,
                        message_id=processing.id
                    )
                    return
                if video.filesize >= 500000000:
                    await client.send_message(
                        text=messages['filesize_pending'],
                        chat_id=update.message.chat.id
                    )
                high_res_video = video.download()
                await client.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=messages['success_message'],
                    message_id=processing.id
                )
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_document(chat_id=update.message.chat.id,
                                           document=high_res_video,
                                           caption=caption)
                if os.path.exists(high_res_video):
                    os.remove(high_res_video)

                await client.send_message(
                    update.message.chat.id,
                    messages['finished_message'],
                )
            except Exception as err:
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=ID,
                                          text=f'There has been an error:\n\n{err}')

        except Exception:
            await client.delete_messages(chat_id=update.message.chat.id,
                                         message_ids=processing.id)
            await client.send_message(chat_id=update.message.chat.id,
                                      text=messages['error_message'])

    elif update.data == 'audio_callback_data':
        processing = await client.edit_message_text(
            text=messages['process_message'],
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        try:
            link = update.message.text
            audio = YouTube(link.split("\n\n", 1)[1])
            caption = f"**{audio.title}**\n\n" \
                      f"Channel - **[{audio.author}]({audio.channel_url})**"
            audio = audio.streams.get_audio_only()
            try:
                await client.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=messages['success_message'],
                    message_id=processing.id
                )
                out_file = audio.download()
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                base, ext = os.path.splitext(out_file)
                new_file = base + ".mp3"
                os.rename(out_file, new_file)
                await client.send_audio(chat_id=update.message.chat.id,
                                        audio=new_file,
                                        caption=caption)
                if os.path.exists(new_file):
                    os.remove(new_file)
                await client.send_message(
                    update.message.chat.id,
                    messages['finished_message'],
                )
            except Exception as err:
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=ID,
                                          text=f'There has been an error:\n\n{err}')

        except Exception:
            await client.delete_messages(chat_id=update.message.chat.id,
                                         message_ids=processing.id)
            await client.send_message(chat_id=update.message.chat.id,
                                      text=messages['error_message'])

    elif update.data == 'playlist_video_callback_data':
        processing = await client.edit_message_text(
            text=messages['process_message'],
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        try:
            link = update.message.text
            playlist = Playlist(link.split("\n\n", 1)[1])
            try:
                for playlist_video in playlist.videos:
                    video = playlist_video.streams.get_highest_resolution()
                    if video.filesize >= 2097152000:
                        await client.send_message(
                            text=messages['filesize_error'],
                            chat_id=update.message.chat.id
                        )
                        return

                    downloaded_video = video.download()
                    await client.delete_messages(
                        chat_id=update.message.chat.id,
                        message_ids=processing.id)
                    await client.send_document(
                        chat_id=update.message.chat.id,
                        document=downloaded_video,
                        caption=f"**{playlist_video.title}**\n\n" \
                                f"Playlist - **[{playlist.title}]({playlist.playlist_url})**\n"
                                f"Channel - **[{playlist_video.author}]({playlist_video.channel_url})**"
                    )
                    if os.path.exists(downloaded_video):
                        os.remove(downloaded_video)
                await client.send_message(chat_id=update.message.chat.id,
                                          text='All done, finished.')
            except KeyError:
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=update.message.chat.id,
                                          text=messages['wrong_button'])
        except Exception as err:
            await client.delete_messages(chat_id=update.message.chat.id,
                                         message_ids=processing.id)
            await client.send_message(chat_id=ID,
                                      text=f'There has been an error:\n\n{err}')

    elif update.data == 'playlist_audio_callback_data':
        processing = await client.edit_message_text(
            text=messages['process_message'],
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        try:
            link = update.message.text
            playlist = Playlist(link.split("\n\n", 1)[1])
            try:
                for playlist_video in playlist.videos:
                    audio = playlist_video.streams.get_audio_only()
                    out_file = audio.download()
                    await client.delete_messages(
                        chat_id=update.message.chat.id,
                        message_ids=processing.id)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + ".mp3"
                    os.rename(out_file, new_file)

                    await client.send_audio(
                        chat_id=update.message.chat.id,
                        audio=new_file,

                        caption=f"**{playlist_video.title}**\n\n" \
                                f"Playlist - **[{playlist.title}]({playlist.playlist_url})**\n"
                                f"Channel - **[{playlist_video.author}]({playlist_video.channel_url})**"
                    )

                    if os.path.exists(new_file):
                        os.remove(new_file)
                await client.send_message(chat_id=update.message.chat.id,
                                          text=messages['finished_message'])
            except KeyError:
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=update.message.chat.id,
                                          text=messages['wrong_button'])
        except Exception as err:
            await client.delete_messages(chat_id=update.message.chat.id,
                                         message_ids=processing.id)
            await client.send_message(chat_id=update.message.chat.id,
                                      text=messages['error_message'])
            await client.send_message(chat_id=ID,
                                      text=f'There has been an error:\n\n{err}')

    elif update.data == 'thumbnail_callback_data':
        processing = await client.edit_message_text(
            text=messages['process_message'],
            chat_id=update.message.chat.id,
            message_id=update.message.id
        )
        try:
            link = update.message.text.split("\n\n", 1)[1]
            video = YouTube(link)
            photo = Thumbnail(link)
            caption = f"**{video.title}**\n\n" \
                      f"Channel - **[{video.author}]({video.channel_url})**"
            try:
                photo.fetch()
                ready_photo = photo.save('.')
                await client.edit_message_text(
                    chat_id=update.message.chat.id,
                    text=messages['success_message'],
                    message_id=processing.id
                )
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_photo(chat_id=update.message.chat.id,
                                        photo=ready_photo,
                                        caption=caption)
                if os.path.exists(ready_photo):
                    os.remove(ready_photo)
                await client.send_message(
                    update.message.chat.id,
                    messages['finished_message'],
                )
            except Exception as err:
                await client.delete_messages(chat_id=update.message.chat.id,
                                             message_ids=processing.id)
                await client.send_message(chat_id=ID,
                                          text=f'There has been an error:\n\n{err}')
        except Exception:
            await client.delete_messages(chat_id=update.message.chat.id,
                                         message_ids=processing.id)
            await client.send_message(chat_id=update.message.chat.id,
                                      text=messages['error_message'])


print('Youtube Downloader has started')
if __name__ == "__main__":
    bot.run()
print('Youtube Downloader has stopped')
