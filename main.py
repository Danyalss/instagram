import requests
import json
import telebot
import time

# اطلاعات ربات را تعریف کنیم
bot = telebot.TeleBot("6583320212:AAHGM6UqfTdHoZjLDmr4RTkTglwpMhwx4N4")

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
            f.write(requests.get(media_url).content)
    elif file_type == "VIDEO":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(media_url).content)
    elif file_type == "REELS":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(media_url).content)
    elif file_type == "STORY":
        with open(file_type + ".jpg", "wb") as f:
            f.write(requests.get(media_url).content)
    elif file_type == "IGTV":
        with open(file_type + ".mp4", "wb") as f:
            f.write(requests.get(media_url).content)

# تابع برای دریافت دستورات را تعریف کنیم
def handle_command(update):
    command = update.message.text

    if command == "/help":
        bot.send_message(update.chat_id, "این ربات به شما امکان می دهد تا محتوای اینستاگرام را دانلود کنید. برای دانلود محتوا، لینک آن را به من ارسال کنید.")
    elif command == "/about":
        bot.send_message(update.chat_id, "این ربات توسط [نام توسعه دهنده] ساخته شده است. برای اطلاعات بیشتر، به [لینک وب سایت توسعه دهنده] مراجعه کنید.")
    else:
        # لینک محتوا را از پیام دریافت کنیم
        media_url = update.message.text

        # محتوا را دانلود کنیم
        media_info = get_media_info(media_url)
        if media_info is not None:
            download_media(media_info)
            bot.send_message(update.chat_id, "محتوا با موفقیت دانلود شد.")

# تابع برای شروع ربات را تعریف کنیم
def start():
    # ربات را در حالت polling اجرا کنیم
    bot.polling()

# تابع اصلی را تعریف کنیم
if __name__ == "__main__":
    # ربات را شروع کنیم
    start()
