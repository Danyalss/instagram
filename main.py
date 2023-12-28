import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from instapy import InstaPy

# Replace with your own Telegram bot token
TELEGRAM_BOT_TOKEN = '6583320212:AAGci8mHu1_ctX1OIQd2rlvqHM-11FIGsZ4'

# Replace with your own Instagram username and password
INSTAGRAM_USERNAME = 'danyalsoltani872@gmail.com'
INSTAGRAM_PASSWORD = 'd/reset/confirm/?uidb36=nzx5l4v&token'

# Create directories to store downloaded images
os.makedirs('downloads', exist_ok=True)

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Send me an Instagram post URL to download the image.')

def download_image(url: str) -> str:
    response = requests.get(url)
    image_filename = url.split('/')[-1]
    with open(os.path.join('downloads', image_filename), 'wb') as f:
        f.write(response.content)
    return image_filename

def download_instagram_image(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if 'instagram.com' not in url:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Invalid Instagram post URL.')
        return

    # Log in to Instagram using InstaPy
    session = InstaPy(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    session.login()

    # Download the image
    image_filename = download_image(url)

    # Log out of Instagram
    session.end()

    # Send the downloaded image back to the user
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(os.path.join('downloads', image_filename), 'rb'))
    os.remove(os.path.join('downloads', image_filename))

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('download', download_instagram_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()