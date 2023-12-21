from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Insert your bot's token here
TOKEN = 'YOUR_BOT_TOKEN'

# Replace this with your bot's username
BOT_USERNAME = 'Dd_instagrambot'

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("افزودن به گروه به عنوان مدیر", callback_data='add_to_group')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('لطفاً گزینه مورد نظر را انتخاب کنید:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    # Add your logic for different callback_data values here
    if query.data == 'add_to_group':
        query.message.reply_text(
            f'برای افزودن بات به گروه خود به عنوان مدیر، از لینک زیر استفاده کنید:\nt.me/{BOT_USERNAME}?startgroup=true'
        )

# In case of error this function will be called
def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, context.error)

# Main function where we initialize handlers and start the bot
def main():
    updater = Updater("6583320212:AAGci8mHu1_ctX1OIQd2rlvqHM-11FIGsZ4", use_context=True)
    dp = updater.dispatcher

    # Handlers for Telegram commands
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
