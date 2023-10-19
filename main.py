import requests
import json
import telebot
import time

# اطلاعات ربات را تعریف کنیم
bot = telebot.TeleBot("YOUR_BOT_TOKEN")

# تابع برای دریافت اطلاعات رسانه را تعریف کنیم
def get_media_info(media_url):
    response = requests.get(media_url)

    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        return None

# تابع برای دانلود رسانه را تعریف کنیم
def download_media(media_info):
    file_type = media_info["media_type"]
    file_url = media_info["media_url"]

    if file_type == "IMAGE":
        with open(file_type + ".jpg", "wb") as f:
            f.write(requests.get(file_url).content)
    elif file_type == "VIDEO":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(file_url).content)
    elif file_type == "REELS":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(file_url).content)
    elif file_type == "STORY":
        with open(file_type + ".jpg", "wb") as f:
            f.write(requests.get(file_url).content)
    elif file_type == "IGTV":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(file_url).content)

# تابع برای دریافت دستورات را تعریف کنیم
@bot.message_handler(commands=["start"])
def handle_start(message):
    # پیام خوش آمدگویی را ارسال کنیم.
    bot.send_message(message.chat.id, "سلام! من ربات دانلود ریلز و استوری و پست اینستاگرام هستم. برای دانلود محتوا، لینک آن را به من ارسال کنید.")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # URL محتوا را دریافت کنید و سپس آن را دانلود کنید.
    media_info = get_media_info(message.text)
    if media_info is not None:
        download_media(media_info)

# تابع برای شروع ربات را تعریف کنیم
def start():
    # ربات را در حالت polling اجرا کنیم
    bot.polling()

# تابع اصلی را تعریف کنیم
if __name__ == "__main__":
    # ربات را شروع کنیم
    start()
