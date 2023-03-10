# Importing dependencies
import os.path
import sqlite3

import validators
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message, ForceReply
from pythumb import Thumbnail
from pytube import YouTube, Playlist

from data import messages, support_text
from keyboards import (
    main_keyboard,
    support_keyboard,
    back_button,
    support_button
)
from secret import (
    API_ID,
    API_HASH,
    ID,
    BOT_TOKEN
)

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
        text=f"**Hello, {message.from_user.first_name}!**\n\n" +
             messages['welcome_text'],
        disable_web_page_preview=False,
        reply_markup=support_button
    )


@bot.on_message(filters.command(commands=['support']) & filters.private)
async def support(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text=support_text['initial_message'],
        reply_markup=support_keyboard
    )


@bot.on_callback_query(filters.regex('support_button'))
async def get_support(client: Client, update: CallbackQuery):
    if update.data == 'support_button':
        try:
            await update.edit_message_text(
                text=support_text['initial_message'],
                disable_web_page_preview=True,
                reply_markup=support_keyboard
            )
        except Exception:
            pass


@bot.on_callback_query(filters.regex('paypal'))
async def paypal_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'paypal_button':
        try:
            await update.edit_message_text(
                text=support_text['paypal_message'],
                disable_web_page_preview=True,
                reply_markup=back_button
            )
        except Exception:
            pass


@bot.on_callback_query(filters.regex('contact'))
async def contact_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'contact_button':
        try:
            await update.edit_message_text(
                text=support_text['contact_message'],
                disable_web_page_preview=True,
                reply_markup=back_button
            )
        except Exception:
            pass


@bot.on_callback_query(filters.regex('back_button'))
async def back_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'back_button':
        try:
            await update.edit_message_text(
                text=support_text['initial_message'],
                disable_web_page_preview=True,
                reply_markup=support_keyboard
            )
        except Exception:
            pass


@bot.on_callback_query(filters.regex('back_to_main'))
async def back_handler(client: Client, update: CallbackQuery) -> None:
    if update.data == 'back_to_main':
        try:
            await update.edit_message_text(
                text=f"**Hello, {update.from_user.first_name}!**\n\n" +
                     messages['welcome_text'],
                disable_web_page_preview=True,
                reply_markup=support_button
            )
        except Exception:
            pass


@bot.on_message(filters.command(["postman"]) & filters.private)
async def postman(client: Client, update: Message) -> None:
    if update.chat.id == int(ID):
        await update.reply_text(
            text="Your message will be sent to everyone.",
            reply_markup=ForceReply(
                placeholder="Postman"
            )
        )


@bot.on_message(filters.command(["message"]) & filters.private)
async def message(client: Client, update: Message) -> None:
    if update.chat.id == int(ID):
        await update.reply_text(
            text="First comes **chat_id** and then your **message**",
            reply_markup=ForceReply(
                placeholder="Message to"
            )
        )


@bot.on_message(filters.command(commands=['get_users']) & filters.private)
async def get_users(client: Client, message: Message):
    if message.chat.id == int(ID):
        connection = sqlite3.connect("YoutubeDownloader.session")
        crsr = connection.cursor()
        crsr.execute("SELECT DISTINCT(id) FROM peers WHERE type == 'user';")
        users_ids = crsr.fetchall()

        await client.send_message(
            chat_id=ID,
            text=f"There are **{len(users_ids)}** users."
        )


@bot.on_message(filters.command(commands=['check_user']) & filters.private)
async def get_check_user(client: Client, update: Message) -> None:
    user_id = update.text.split(' ')[1]

    connection = sqlite3.connect("YoutubeDownloader.session")
    crsr = connection.cursor()
    crsr.execute(f"SELECT * FROM peers WHERE id == {user_id};")
    user = crsr.fetchall()

    try:
        await client.send_message(
            chat_id=ID,
            text=f"User ID: **{user[0][0]}**\n"
                 f"Type: **{user[0][2]}**\n"
                 f"Username: **{user[0][3]}**\n"
                 f"Phone number: **{user[0][4]}**\n"
                 f"Last updated: **{user[0][5]}**\n"
        )
    except Exception as err:
        await client.send_message(
            chat_id=ID,
            text=f'User **{user_id}** not found in the dababase.\n\n'
                 f'Log: **{user}**\n\n'
                 f'Exception: **{err}**'
        )


@bot.on_message(filters.command(commands=['admin']) & filters.private)
async def get_admin_menu(client: Client, message: Message):
    if message.chat.id == int(ID):
        await client.send_message(
            chat_id=ID,
            text=f"**Dear {message.chat.first_name}**\n\n"
                 f"/start - to start the bot\n\n"
                 f"/get_users - to count all users\n\n"
                 f"/check_user - to check if user exists\n\n"
                 f"/message - to send message to one user\n\n"
                 f"/postman - to send message to all\n\n"
        )


@bot.on_message(filters.private)
async def download(client: Client, update: Message) -> None:
    if update.reply_to_message:
        if update.reply_to_message.reply_markup.placeholder == "Postman":
            connection = sqlite3.connect("YoutubeDownloader.session")
            crsr = connection.cursor()
            crsr.execute(
                "SELECT DISTINCT(id) FROM peers WHERE type == 'user';")
            users_ids = crsr.fetchall()

            for user_id in users_ids:
                id = int(user_id[0])
                try:
                    await client.send_message(
                        chat_id=id,
                        text=update.text,
                        disable_notification=True
                    )
                except Exception as err:
                    await client.send_message(
                        ID,
                        text=f'Error:\n\n{err}'
                    )

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
                        text=text,
                        disable_notification=True
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
            reply_markup=main_keyboard,
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
