from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

HEIGHT, WEIGHT = range(2)

def bmi(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'What is your height(cm)?\n\n'
        'Send /cancel to stop talking to me.\n',
    )
    return HEIGHT

def height(update: Update, _: CallbackContext) -> int:
    global height_input 
    try:
        height_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'Thats not a valid input!\n'
            'What is your height(cm)?\n'
        )   
        return HEIGHT 
    height_input = height_input/100    
    update.message.reply_text('What is your weight(kg)?')
    return WEIGHT

def weight(update: Update, _: CallbackContext) -> int:
    global weight_input 
    weight_status = ""
    try:
        weight_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'That is an invalid input!\n'
            'What is your weight(kg)?\n'
        )   
        return WEIGHT 
    bmi = weight_input / (height_input*height_input)
    bmi_str = "{:.2f}".format(bmi)
    if bmi < 18.50 :
        weight_status = 'Your weight status is: Underweight'
    elif 18.50 <= bmi < 25.00:
        weight_status = 'Your weight status is: Normal/Healthy Weight'
    elif 25.00 <= bmi < 30.00:
        weight_status = 'Your weight status is: Overweight'
    else: 
        weight_status = 'Your weight status is: Obese'
    update.message.reply_text(
        'Your BMI is: ' + bmi_str + '\n' + weight_status
    )
    
    return ConversationHandler.END
    