from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

def helps(update, context):
    update.message.reply_text(
        f"{'-'*44}\n"
        '/help : Information to commands\n'
        '/calories : Receive calories of food intake\n'
        '/healthfacts : Obtain health tips and facts\n'
        '/bmi : Calculate your bmi\n'
        '/reminderbreakfast : Set breakfast reminder\n'
        '/reminderlunch : Set lunch reminder\n'
        '/reminderdinner : Set dinner reminder\n'
        '/unsetbreakfast : Unset breakfast reminder\n'
        '/unsetlunch : Unset lunch reminder\n'
        '/unsetdinner : Unset dinner reminder\n'
        '/diary dd/mm/yyyy : Check food diary\n'
        '/removeitem dd/mm/yyyy : Remove food entry\n'
        '/quiz : Quiz to test your knowledge\n'
        '/cancel : Cancel current command\n'
        f"{'-'*44}\n"
    )


