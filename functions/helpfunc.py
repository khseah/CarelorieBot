from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

def help(update, context):
    update.message.reply_text(
        f"{'-'*44}\n"
        '/help : Information to commands\n'
        '/calories : Receive calories of food intake\n'
        '/healthfacts : Obtain health tips and facts\n'
        '/bmi : Calculate your bmi\n'
        '/cancel : Cancel current command\n'
        f"{'-'*44}\n"
    )


