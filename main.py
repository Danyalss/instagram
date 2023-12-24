import telebot
from telebot import types
import time

API_TOKEN = '6583320212:AAGci8mHu1_ctX1OIQd2rlvqHM-11FIGsZ4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                # كاربر تگ شده است
                user_id = entity.user.id
                chat_id = message.chat.id
                try:
                    user_status = bot.get_chat_member(chat_id, user_id).status
                    if user_status:
                        # هنگامی که کاربر حالت last_seen فعال داشته باشد
                        if user_status in ['online', 'recently', 'within_week', 'within_month']:
                            bot.reply_to(message, f'کاربر {entity.user.first_name} انلاین است')
                        else:
                            bot.reply_to(message, f'کاربر {entity.user.first_name} افلاین است')
                except Exception as e:
                    bot.reply_to(message, 'خطا در بررسی وضعیت کاربر.')

bot.polling()