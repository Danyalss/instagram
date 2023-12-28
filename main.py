import os
import subprocess
import tempfile
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = "YOUR_BOT_TOKEN"

# The Instagram webpage URL that you want to download posts from
INSTAGRAM_WEBPAGE_URL = "https://www.instagram.com/explore/tags/your-hashtag/"

def install_phantomjs():
    subprocess.check_output("sudo apt-get install phantomjs", shell=True)

def download_instagram_webpage():
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)
    subprocess.check_output(["phantomjs", "--ssl-protocol=any", "--ignore-ssl-errors=true", "/path/to/instagram_webpage_renderer.js", INSTAGRAM_WEBPAGE_URL])
    return temp_dir

def send_downloaded_image(update: Update, context: CallbackContext):
    temp_dir = download_instagram_webpage()
    with open("temp.jpg", "rb") as img:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)
    os.remove("temp.jpg")
    os.rmdir(temp_dir)

def main():
    try:
        install_phantomjs()
    except Exception as e:
        print(f"PhantomJS installation failed: {e}")
        return

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    def start(update: Update, context: CallbackContext):
        update.message.reply_text('Hi! Use /download to download the latest photo from Instagram.')

    def download(update: Update, context: CallbackContext):
        send_downloaded_image(update, context)

    start_handler = CommandHandler("start", start)
    download_handler = CommandHandler("download", download)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()