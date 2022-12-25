from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

messages = {
    'welcome_text': '🤖This bot can help you to download anything from YouTube For Free!\n\n'
                    '📥Send your Youtube link here!\n\n'
                    '**💗Enjoy**',
    'error_message': f'🇬🇧 Error! Please send YouTube link and choose proper command.\n\n'
                     f'🇷🇺 Ошибка! Пожалуйста, отправьте ссылку на YouTube и выберите правильную команду.',
    'filesize_error': f'🇬🇧 Error! Video exceeds 2GB, we cannot send it.\n\n'
                      f'🇷🇺 Ошибка! Видео превышает 2 ГБ, мы не можем его отправить',
    'filesize_pending': f'🇬🇧 Please wait, your file is too big, it will take some minutes.\n\n'
                        f'🇷🇺 Пожалуйста, подождите, ваш файл слишком большой, это займет несколько минут.',
    'success_message': f"🇬🇧 Success! We'll send it shortly!\n\n"
                       f'🇷🇺 Отправляю вам файл!',
    'process_message': f'🇬🇧 Processing your request...\n\n'
                       f'🇷🇺 Обработка вашего запроса...',
    'finished_message': f'🇬🇧 All done, finished.\n\n'
                        f'🇷🇺 Все готово, закончено.',
    'wrong_button': f'🇬🇧 Error! Wrong action, please choose proper command.\n\n'
                    f'🇷🇺 Ошибка! Неправильное действие, пожалуйста, выберите правильную команду.'
}

support_text = {
    'initial_message': 'Thank you for your interest in helping this project! You can contribute in two ways:\n\n'
                       '1. Offer your technical expertise as a developer👨🏻‍💻\n'
                       '2. Donate money to help the developer buy a Raspberry Pi, which keeps the bot online🚀\n\n'
                       'Your support is greatly appreciated. Thank you for helping us make this project a success!!',
    'paypal_message': 'Thank you for showing interest!\n\n'
                      'Your donation can help the developer purchase a Raspberry Pi, keeping the bot online and available to millions. '
                      'Your generosity makes a difference. Thank you!\n\n'
                      "PayPal address to donate 👉 `@mirabbosdev`",
    'contact_message': 'Thank you for showing interest!\n\n'
                       'Feel free to text and discuss your project idea 👉 @mirabbos_dev'
}

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