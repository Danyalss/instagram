from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

def check_status(update: Update, context: CallbackContext):
    msg = update.message.reply_to_message

    # اطمینان حاصل کنید که پیام یک تگ است.
    if msg:
        user_id = msg.from_user.id
        chat_id = update.message.chat_id
        
        try:
            user_member = context.bot.get_chat_member(chat_id, user_id)
            user_status = user_member.status

            # بر اساس وضعیت تعیین می‌کنیم که کاربر آنلاین است یا نه
            if user_status in ['online', 'recently']:
                status_message = "انلاین است"
            else:
                status_message = "افلاین است"

            # پیامی ارسال کنید که وضعیت را گزارش می‌دهد
            update.message.reply_text(f"کاربر {status_message}")

        except Exception as e:
            # در صورت بروز خطا، پیام خطا پرینت شود.
            print(f"خطا: {e}")
            update.message.reply_text("خطا در دریافت وضعیت کاربر.")
    else:
        update.message.reply_text("لطفاً یک پیام را برای بررسی وضعیت تگ کنید.")

def main():
    # توکن ربات خود را اینجا قرار دهید
    updater = Updater("6583320212:AAGci8mHu1_ctX1OIQd2rlvqHM-11FIGsZ4", use_context=True)

    dp = updater.dispatcher

    # هندلر برای پاسخ به تگ‌های پیام
    dp.add_handler(MessageHandler(Filters.reply & Filters.text, check_status))

    # شروع نظرخواهی از سرور تلگرام
    updater.start_polling()

    # اجازه دهید ربات تا زمانی که پردازش انجام می‌گیرد، فعال بماند
    updater.idle()

if __name__ == '__main__':
    main()