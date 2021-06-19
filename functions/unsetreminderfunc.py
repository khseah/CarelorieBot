from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

def unsetbreakfast(update: Update, context: CallbackContext) -> None:
    if context.job_queue.get_jobs_by_name('breakfast'):
        for job in context.job_queue.get_jobs_by_name('breakfast'):
            job.schedule_removal()
        update.message.reply_text(u"\U0001F515" + 'Breakfast reminder successfully removed!')
    else:
        update.message.reply_text('Please set a reminder first\n' + '/reminderbreakfast')

def unsetlunch(update: Update, context: CallbackContext) -> None:
    if context.job_queue.get_jobs_by_name('lunch'):
        for job in context.job_queue.get_jobs_by_name('lunch'):
            job.schedule_removal()
        job_names = [job.name for job in context.job_queue.jobs()]
        update.message.reply_text(u"\U0001F515" + 'Lunch reminder successfully removed!')
    else:
         update.message.reply_text('Please set a reminder first\n' + '/reminderlunch')

def unsetdinner(update: Update, context: CallbackContext) -> None:
    if context.job_queue.get_jobs_by_name('dinner'):
        for job in context.job_queue.get_jobs_by_name('dinner'):
            job.schedule_removal()
        update.message.reply_text(u"\U0001F515" + 'Dinner reminder successfully removed!')
    else:
        update.message.reply_text('Please set a reminder first\n' + '/reminderdinner')