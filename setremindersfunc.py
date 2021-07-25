import datetime, pytz

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

HOUR_B, MIN_B, HOUR_L, MIN_L, HOUR_D, MIN_D = range(6)

def breakfast(context: CallbackContext) -> None: #Reminder message for breakfast
    job = context.job
    context.bot.send_message(job.context, text= u"\uE325" +'Time to input what you ate for breakfast'  + u"\uE325" + '\n\n' + "Let's go /calories")

def lunch(context: CallbackContext) -> None: #Reminder message for lunch
    job = context.job
    context.bot.send_message(job.context, text=u"\uE325" + 'Time to input what you ate for lunch' + u"\uE325" + '\n\n' + "Let's go /calories")

def dinner(context: CallbackContext) -> None: #Reminder message for dinner
    job = context.job
    context.bot.send_message(job.context, text=u"\uE325" + 'Time to input what you ate for dinner' + u"\uE325" + '\n\n' + "Let's go /calories")

def reminderbreakfast(update: Update, context: CallbackContext) -> int:
    if context.job_queue.get_jobs_by_name('breakfast'):
        hour = '0' + str(hour_b_input) if hour_b_input < 10 else str(hour_b_input)
        minute = '0' + str(min_b_input) if min_b_input < 10 else str(min_b_input)
        day = ' AM' if hour_b_input < 12 else ' PM'
        update.message.reply_text(
            'You have an existing reminder at ' + str(hour) + ':' + str(minute) + day + '\n\n'
            'To set a new reminder, you have to\n' + '/unsetbreakfast first'
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            u"\uE325" + 'SETTING REMINDER FOR BREAKFAST' + u"\uE325" + '\n\n'
            'Which HOUR would you like to set? 0-23\n\n'
            'Send /cancel to stop talking to me.\n',
        )
        return HOUR_B

def hour_b(update: Update, _: CallbackContext) -> int:
    global hour_b_input 
    try:
        hour_b_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'Thats not a valid input!\n'
            'Which HOUR would you like to set? 0-23\n'
        )   
        return HOUR_B  
    update.message.reply_text(
        'Which MINUTE would you like to set? 0-59\n\n'
        'Send /cancel to stop talking to me.\n',
    )
    return MIN_B

def min_b(update: Update, context: CallbackContext) -> int:
    global min_b_input 
    try:
        min_b_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'That is an invalid input!\n'
            'Which MINUTE would you like to set? 0-59\n'
        )   
        return MIN_B
    t = datetime.time(hour_b_input, min_b_input,00,000000,tzinfo = pytz.timezone('Asia/Singapore'))
    context.job_queue.run_daily(breakfast, t, days= (0,1,2,3,4,5,6), context=update.message.chat_id)
    hour = '0' + str(hour_b_input) if hour_b_input < 10 else str(hour_b_input)
    minute = '0' + str(min_b_input) if min_b_input < 10 else str(min_b_input)
    day = ' AM' if hour_b_input < 12 else ' PM'
    update.message.reply_text('Breakfast reminder has been set at '+ str(hour) + ':' + str(minute) + day)

    return ConversationHandler.END

def reminderlunch(update: Update, context: CallbackContext) -> int:
    if context.job_queue.get_jobs_by_name('lunch'):
        hour = '0' + str(hour_l_input) if hour_l_input < 10 else str(hour_l_input)
        minute = '0' + str(min_l_input) if min_l_input < 10 else str(min_l_input)
        day = ' AM' if hour_l_input < 12 else ' PM'
        update.message.reply_text(
            'You have an existing reminder at ' + str(hour) + ':' + str(minute) + day + '\n\n'
            'To set a new reminder, you have to\n' + '/unsetlunch first'
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            u"\uE325" + 'SETTING REMINDER FOR LUNCH' + u"\uE325" + '\n\n'
            'Which HOUR would you like to set? 0-23\n\n'
            'Send /cancel to stop talking to me.\n',
        )
        return HOUR_L

def hour_l(update: Update, _: CallbackContext) -> int:
    global hour_l_input 
    try:
        hour_l_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'Thats not a valid input!\n'
            'Which HOUR would you like to set? 0-23\n'
        )   
        return HOUR_L 
    update.message.reply_text(
        'Which MINUTE would you like to set? 0-59\n\n'
        'Send /cancel to stop talking to me.\n',
    )
    return MIN_L

def min_l(update: Update, context: CallbackContext) -> int:
    global min_l_input 
    try:
        min_l_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'That is an invalid input!\n'
            'Which MINUTE would you like to set? 0-59\n'
        )   
        return MIN_L
    t = datetime.time(hour_l_input, min_l_input,00,000000,tzinfo = pytz.timezone('Asia/Singapore'))
    context.job_queue.run_daily(lunch, t, days= (0,1,2,3,4,5,6), context=update.message.chat_id)
    hour = '0' + str(hour_l_input) if hour_l_input < 10 else str(hour_l_input)
    minute = '0' + str(min_l_input) if min_l_input < 10 else str(min_l_input)
    day = ' AM' if hour_l_input < 12 else ' PM'
    update.message.reply_text('Lunch reminder has been set at ' + str(hour) + ':' + str(minute) + day)

    return ConversationHandler.END

def reminderdinner(update: Update, context: CallbackContext) -> int:
    if context.job_queue.get_jobs_by_name('dinner'):
        hour = '0' + str(hour_d_input) if hour_d_input < 10 else str(hour_d_input)
        minute = '0' + str(min_d_input) if min_d_input < 10 else str(min_d_input)
        day = ' AM' if hour_d_input < 12 else ' PM'
        update.message.reply_text(
            'You have an existing reminder at ' + str(hour) + ':' + str(minute) + day + '\n\n'
            'To set a new reminder, you have to\n' + '/unsetdinner first'
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            u"\uE325" + 'SETTING REMINDER FOR DINNER' + u"\uE325" + '\n\n'
            'Which HOUR would you like to set? 0-23\n\n'
            'Send /cancel to stop talking to me.\n',
        )
        return HOUR_D

def hour_d(update: Update, _: CallbackContext) -> int:
    global hour_d_input 
    try:
        hour_d_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'Thats not a valid input!\n'
            'Which HOUR would you like to set? 0-23\n'
        )   
        return HOUR_L 
    update.message.reply_text(
        'Which MINUTE would you like to set? 0-59\n\n'
        'Send /cancel to stop talking to me.\n',
    )
    return MIN_D

def min_d(update: Update, context: CallbackContext) -> int:
    global min_d_input 
    try:
        min_d_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'That is an invalid input!\n'
            'What min would you like to set it at? 0-59\n'
        )   
        return MIN_D
    t = datetime.time(hour_d_input, min_d_input,00,000000,tzinfo = pytz.timezone('Asia/Singapore'))
    context.job_queue.run_daily(dinner, t, days= (0,1,2,3,4,5,6), context=update.message.chat_id)
    hour = '0' + str(hour_d_input) if hour_d_input < 10 else str(hour_d_input)
    minute = '0' + str(min_d_input) if min_d_input < 10 else str(min_d_input)
    day = ' AM' if hour_d_input < 12 else ' PM'
    update.message.reply_text('Dinner reminder has been set at ' + str(hour) + ':' + str(minute) + day)

    return ConversationHandler.END

