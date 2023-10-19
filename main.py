import requests
import json
import telebot

bot = telebot.TeleBot("6583320212:AAHGM6UqfTdHoZjLDmr4RTkTglwpMhwx4N4")

def start(update):
    # ID کاربر یا گروهی که پیام از آن ارسال شده است را دریافت کنیم.
    chat_id = update.message.chat_id

    # پیام خوش آمدگویی را ارسال کنیم.
    bot.send_message(chat_id, "سلام! من ربات دانلود ریلز و استوری و پست اینستاگرام هستم. برای دانلود محتوا، لینک آن را به من ارسال کنید.")

def handle_message(update):
    # لینک محتوا را از پیام دریافت کنیم.
    media_url = update.message.text

    # محتوا را دانلود کنیم.
    media_info = get_media_info(media_url)
    if media_info is not None:
        download_media(media_info)
        bot.send_message(update.chat_id, "محتوا با موفقیت دانلود شد.")

def get_media_info(media_url):
    response = requests.get(media_url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        return None

def download_media(media_info):
    file_type = media_info["media_type"]
    file_url = media_info["media_url"]

    if file_type == "IMAGE":
        with open(file_type + ".jpg", "wb") as f:
           f.write(requests.get(media_info["media_url"]).content)
    elif file_type == "VIDEO":
        with open(file_type + ".mp4", "wb") as f:
           f.write(requests.get(media_info["media_url"]).content)
    elif file_type == "REELS":
        with open(file_type + ".mp4", "wb") as f:
           f.write(requests.get(media_info["media_url"]).content)
    elif file_type == "STORY":
        with open(file_type + ".jpg", "wb") as f:
           f.write(requests.get(media_info["media_url"]).content)
    elif file_type == "IGTV":
        with open(file_type + ".mp4", "wb") as f:
           f.write(requests.get(media_info["media_url"]).content)

def handle_command(update):
    command = update.message.text

    if command == "/help":
        bot.send_message(update.chat_id, "این ربات به شما امکان می دهد تا محتوای اینستاگرام را دانلود کنید. برای دانلود محتوا، لینک آن را به من ارسال کنید.")
    elif command == "/about":
        bot.send_message(update.chat_id, "این ربات توسط [نام توسعه دهنده] ساخته شده است. برای اطلاعات بیشتر، به [لینک وب سایت توسعه دهنده] مراجعه کنید.")
    else:
        bot.send_message(update.chat_id, "دستور نامعتبر")

def main():
    # ربات را در حالت polling اجرا کنیم.
    bot.polling()

if __name__ == "__main__":
    main()
