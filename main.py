import logging
import requests
import datetime, pytz
from dotenv import load_dotenv
import os
PORT = int(os.environ.get('PORT', 5000))
load_dotenv()


from functions.helpfunc import helps
from functions.healthfactsfunc import healthfacts
from functions.unsetreminderfunc import unsetbreakfast, unsetdinner, unsetlunch
from functions.bmifunc import bmi, height, weight
from functions.setremindersfunc import breakfast, lunch, dinner, reminderbreakfast, hour_b, min_b, reminderlunch, hour_l, min_l, reminderdinner, hour_d, min_d
from functions.caloriefunc import calories, add_entry, get_calorie, diary, delete, deleting_item, confirm_delete
from functions.quizfunc import quiz_start, quiz_cancel, quiz_qns

# Set your bot_token here
bot_token = os.getenv("BOT_TOKEN") #input own bot key

# Importing python-telegram-bot's library functions
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Setting up our logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

HEIGHT, WEIGHT = range(2)
FOOD = range(1)
HOUR_B, MIN_B, HOUR_L, MIN_L, HOUR_D, MIN_D = range(6)
QUIZ_QNS = range(1)
DELETEITEM, CONFIRMDELETE = range(2)

# Functions to handle each command
def start(update, context):
    name = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi " + name +", welcome to Careloriebot, a one stop platform to resolve your fitness needs.")

def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Cancelled!\nWhat would you like to find out next?'
    )
    return ConversationHandler.END

# Create and add command handlers
def main() -> None:
    # Setting up their polling stuff
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start) #command handler for /start
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', helps) #command handler for /help
    dispatcher.add_handler(help_handler)


    fact_handler = CommandHandler('healthfacts', healthfacts)
    dispatcher.add_handler(fact_handler)
    
    log_handler = CommandHandler('diary', diary)
    dispatcher.add_handler(log_handler)

    dispatcher.add_handler(CommandHandler("unsetbreakfast", unsetbreakfast)) #unset reminder for breakfast

    dispatcher.add_handler(CommandHandler("unsetlunch", unsetlunch)) #unset reminder for lunch

    dispatcher.add_handler(CommandHandler("unsetdinner", unsetdinner)) #unset reminder for dinner

    conv_handler = ConversationHandler(          #conversation handler for /bmi
        entry_points=[CommandHandler('bmi', bmi)],
        states={
            HEIGHT: [MessageHandler(Filters.text & ~Filters.command, height)],
            WEIGHT: [MessageHandler(Filters.text & ~Filters.command, weight)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(          #conversation handler for /calorie
        entry_points=[CommandHandler('calories', calories)],
        states={
            FOOD: [MessageHandler(Filters.text & ~Filters.command, get_calorie)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    add_handler = CommandHandler('add', add_entry)  #command handler to add food into diary
    dispatcher.add_handler(add_handler)

    conv_handler = ConversationHandler(          #conversation handler for /reminder breakfast
        entry_points=[CommandHandler('reminderbreakfast', reminderbreakfast)],
        states={
            HOUR_B: [MessageHandler(Filters.text & ~Filters.command, hour_b)],
            MIN_B: [MessageHandler(Filters.text & ~Filters.command, min_b)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(          #conversation handler for /reminder lunch
        entry_points=[CommandHandler('reminderlunch', reminderlunch)],
        states={
            HOUR_L: [MessageHandler(Filters.text & ~Filters.command, hour_l)],
            MIN_L: [MessageHandler(Filters.text & ~Filters.command, min_l)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    conv_handler = ConversationHandler(          #conversation handler for /reminder dinner
        entry_points=[CommandHandler('reminderdinner', reminderdinner)],
        states={
            HOUR_D: [MessageHandler(Filters.text & ~Filters.command, hour_d)],
            MIN_D: [MessageHandler(Filters.text & ~Filters.command, min_d)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    quiz_handler = ConversationHandler(         #conversation hanfler for /quiz
        entry_points=[CommandHandler('quiz', quiz_start)],
        states={
            QUIZ_QNS: [MessageHandler(Filters.text & ~Filters.command, quiz_qns)]
        },
        fallbacks=[CommandHandler('cancel', quiz_cancel)],
    )
    dispatcher.add_handler(quiz_handler)

    conv_handler = ConversationHandler(          #conversation handler for /removeitem
        entry_points=[CommandHandler('removeitem', delete)],
        states={
            DELETEITEM: [MessageHandler(Filters.text & ~Filters.command, deleting_item)],
            CONFIRMDELETE: [MessageHandler(Filters.text & ~Filters.command, confirm_delete)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=bot_token)
    updater.bot.setWebhook('https://careloriebot.herokuapp.com/' + bot_token)
    updater.idle() # ensuress that there wont be any clashes

if __name__ == '__main__':
    main()