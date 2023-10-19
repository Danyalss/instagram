import requests
import json
import telebot

bot = telebot.TeleBot("6583320212:AAHGM6UqfTdHoZjLDmr4RTkTglwpMhwx4N4")

def get_media_info(media_url):
    response = requests.get(media_url)
    if response.status_code == 200:
        try:
            data = json.loads(response.content)
        except json.decoder.JSONDecodeError:
            return None

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
    bot.send_message(message.chat_id, "سلام! من ربات دانلود ریلز و استوری و پست اینستاگرام هستم. برای دانلود محتوا، لینک آن را به من ارسال کنید.")

@bot.message_handler(content_types=["text"])
def handle_message(message):
    media_url = message.text
    try:
        media_info = get_media_info(media_url)
    except Exception:
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")
        return

    if media_info["media_type"] == "IMAGE":
        with open(media_info["media_type"] + ".jpg", "wb") as f:
            f.write(requests.get(media_info["media_url"]).content)


@bot.message_handler(commands=["download_image"])
def download_image(message):
    media_url = message.text
    try:
        media_info = get_media_info(media_url)
    except Exception:
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")
        return

    if media_info is not None:
        download_media(media_info)
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")

@bot.message_handler(commands=["download_story"])
def download_story(message):
    media_url = message.text
    try:
        media_info = get_media_info(media_url)
    except Exception:
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")
        return

    if media_info is not None:
        if media_info["media_type"] == "STORY":
            download_media(media_info)
            bot.send_message(message.chat_id, "داستان با موفقیت دانلود شد.")
        else:
            bot.send_message(message.chat_id, "لینک ارسال شده یک داستان نیست.")



    if media_info is not None:
        download_media(media_info)
        bot.send_message(message.chat_id, "محتوا با موفقیت دانلود شد.")

@bot.message_handler(commands=["save_to_folder"])
def save_to_folder(message):
    media_url = message.text
    try:
        media_info = get_media_info(media_url)
    except Exception:
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")
        return

    if media_info is not None:
        download_media(media_info)
        file_type = media_info["media_type"]
        file_name = file_type + ".mp4"
        file_path = f"/path/to/folder/{file_name}"
        with open(file_path, "wb") as f:
            f.write(requests.get(media_info["media_url"]).content)
        bot.send_message(message.chat_id, f"محتوا با موفقیت در پوشه {file_path} ذخیره شد.")

@bot.message_handler(commands=["send_to_chat"])
def send_to_chat(message):
    media_url = message.text
    try:
        media_info = get_media_info(media_url)
    except Exception:
        bot.send_message(message.chat_id, "خطا! مشکلی در دانلود محتوا رخ داد.")
        return

    if media_info is not None:
        download_media(media_info)
        chat_id = message.text
        bot.send_message(chat_id, "محتوا با موفقیت ارسال شد.")

@bot.message_handler(commands=["send_notification"])
def send_notification(message):
    bot.send_message(message.chat_id, "فیلم با موفقیت دانلود شد.")

@bot.message_handler(commands=["help"])
def help(message):
    help_text = """
    **راهنمای استفاده از ربات دانلود ریلز و استوری و پست اینستاگرام:**

    * برای دانلود یک فیلم، دستور `download` را به همراه لینک فیلم ارسال کنید.
    * برای دانلود یک تصویر، دستور `download_image` را به همراه لینک تصویر ارسال کنید.
    * برای ذخیره یک فیلم در یک پوشه خاص، دستور `save_to_folder` را به همراه لینک فیلم و مسیر پوشه را ارسال کنید.
    * برای ارسال یک فیلم به مخاطبین یا گروه های خاص، دستور `send_to_chat` را به همراه لینک فیلم و ID مخاطب یا گروه را ارسال کنید.
    * برای دریافت اعلان زمانی که فیلمی با موفقیت دانلود شد، دستور `send_notification` را ارسال کنید.

    **مثال ها:**

    * برای دانلود یک فیلم:

        `/download https://www.instagram.com/p/Cd4X--_r7t9/`

    * برای دانلود یک تصویر:

        `/download_image https://www.instagram.com/p/Cd4X--_r7t9/`

    * برای ذخیره یک فیلم در پوشه `/downloads`:

        `/save_to_folder https://www.instagram.com/p/Cd4X--_r7t9/ /downloads`

    * برای ارسال یک فیلم به مخاطب با ID `1234567890`:

        `/send_to_chat https://www.instagram.com/p/Cd4X--_r7t9/ 1234567890`
    """
    bot.send_message(message.chat_id, help_text)

bot.polling()
