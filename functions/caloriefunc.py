import requests

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

FOOD = range(1)

def calories(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'What food/drink did you eat?\n\n'
        'For more accurate results, specify:\n'
        'Eg: 1 bowl Laksa\n'
        '(quantity) (measurement) (food/drink)\n'
    )
    return FOOD

def get_calorie(update: Update, _: CallbackContext) -> int:
    global food_input
    food_input = str(update.message.text)
    endpoint = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = food_input
    response = requests.get(endpoint + query, headers={'X-Api-Key': 'YOUR_API_KEY'}) #input own api key
    if not response.json()["items"]:
        update.message.reply_text(
            'Sorry ' + food_input + ' is not in our database\n'
            'Please be more specific\n'
        )
        return FOOD
    else:
        calories = str(response.json()["items"][0]["calories"])
        protein = str(response.json()["items"][0]["protein_g"])
        carbohydrates = str(response.json()["items"][0]["carbohydrates_total_g"])
        fat = str(response.json()["items"][0]["fat_total_g"])
        sugar = str(response.json()["items"][0]["sugar_g"])
        update.message.reply_text(
            'Item name: ' + food_input + '\n\n'
            'Calories(kcal): ' + calories + '\n'
            'Protein(g): ' + protein + '\n'
            'Carohydates(g): ' + carbohydrates + '\n'
            'Sugar(g): ' + sugar + '\n'
            'Fats(g): ' + fat + '\n\n'
            'Press /cancel to finish\n'
            )
    return FOOD
