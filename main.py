import requests
import json
import telebot

bot = telebot.TeleBot("6583320212:AAHGM6UqfTdHoZjLDmr4RTkTglwpMhwx4N4")

def get_media_info(media_url):
    response = requests.get(media_url)
    if response.status_code == 200:
        data = json.loads(response.content)

        if data["media_type"] == "IMAGE":
            return data
        elif data["media_type"] == "VIDEO":
            return data
        elif data["media_type"] == "REELS":
            reels_info = data["media_reels"]
            return {
                "media_type": "REELS",
                "media_url": reels_info["video_url"],
                "media_caption": reels_info["caption"],
            }
        elif data["media_type"] == "STORY":
            story_info = data["media_story"]
            return {
                "media_type": "STORY",
                "media_url": story_info["media_url"],
                "media_caption": story_info["caption"],
            }
        elif data["media_type"] == "IGTV":
            return {
                "media_type": "IGTV",
                "media_url": data["media_igtv"]["video_url"],
                "media_caption": data["media_igtv"]["caption"],
            }
        else:
            return None

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

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "سلام! من ربات دانلود ریلز و استوری و پست اینستاگرام هستم. برای دانلود محتوا، لینک آن را به من ارسال کنید.")

@bot.message_handler(content_types=["text"])
def handle_message(message):
    media_url = message.text
    media_info = get_media_info(media_url)
    if media_info is not None:
        download_media(media_info)
        bot.send_message(message.chat.id, "محتوا با موفقیت دانلود شد.")
    else:
        bot.send_message(message.chat.id, "خطا! لینک معتبری وارد نکرده اید.")

@bot.message_handler(commands=["setprivacy"])
def set_privacy(message):
    privacy = message.text
    if privacy == "public":
        bot.set_privacy("public")
        bot.send_message(message.chat.id, "حالا ربات برای همه قابل مشاهده است.")
    elif privacy == "private":
        bot.set_privacy("private")
        bot.send_message(message.chat.id, "حالا ربات فقط برای کاربرانی که شما را دنبال می کنند قابل مشاهده است.")
    else:
        bot.send_message(message.chat.id, "لطفاً یک حریم خصوصی معتبر وارد کنید.")

bot.polling()
