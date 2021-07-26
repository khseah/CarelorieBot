import requests
import pymongo
from pymongo import MongoClient
import datetime
import pytz
from datetime import date
from dotenv import load_dotenv
import os
load_dotenv()

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
DELETEITEM,CONFIRMDELETE = range(2)

api_key = os.getenv("API_KEY")

cluster_url = os.getenv("CLUSTER_URL")
cluster = MongoClient(cluster_url)
db = cluster["Careloriebot"]
collection = db["Calories"]

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
    global calorie
    global protein
    global carbohydrates
    global fat
    global sugar
    food_input = str(update.message.text)
    endpoint = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = food_input
    response = requests.get(endpoint + query, headers={'X-Api-Key': api_key}) #input own api key
    if not response.json()["items"]:
        update.message.reply_text(
            'Sorry ' + food_input + ' is not in our database\n'
            'Please be more specific\n'
        )
        return FOOD
    else:
        calorie = str(response.json()["items"][0]["calories"])
        protein = str(response.json()["items"][0]["protein_g"])
        carbohydrates = str(response.json()["items"][0]["carbohydrates_total_g"])
        fat = str(response.json()["items"][0]["fat_total_g"])
        sugar = str(response.json()["items"][0]["sugar_g"])
        update.message.reply_text(
            'Item name: ' + food_input + '\n\n'
            'Calories(kcal): ' + calorie + '\n'
            'Protein(g): ' + protein + '\n'
            'Carbohydates(g): ' + carbohydrates + '\n'
            'Sugar(g): ' + sugar + '\n'
            'Fats(g): ' + fat + '\n\n'
            'Press /add to add it to your diary\n'
            'Press /cancel to finish\n'
            )

    return FOOD

def add_entry(update, context):
    update.message.reply_text(food_input + " has been added!")
    
    today = datetime.datetime.today()
    today = today.strftime(f"%d/%m/%Y")
    log = collection.find_one_and_update(
        {"user": update.message.chat_id , "date": today}, #query
        {'$push': {"item" : {"name":food_input, "calories": float(calorie), "protein": float(protein), "fat": float(fat), "sugar": float(sugar)}}}, #what to add to db
        upsert = True) #if theres an existing entry, add it in, else create new entry

    return FOOD

def diary(update, context):
    try: 
        dates = str(context.args[0])
        calories = 0
        text = ""
        find = collection.find({"user" : update.message.chat_id, "date":dates})
        for x in find:
            for y in x["item"]:
                calories += y["calories"]
                text += y["name"] + '\n'

        calories_str = "{:.1f}".format(calories)
        update.message.reply_text(
            dates + '\n\n' + text + '\n' + 'Total calories: ' + str(calories_str) +'kcal'
        )
    except (IndexError, ValueError):
        update.message.reply_text(
            'Please type command in this format\n' +
            'For eg: /diary 23/06/2021'
        )

def delete(update: Update, context: CallbackContext) -> None:
    global delete_date
    try: 
        delete_date = str(context.args[0])
        update.message.reply_text(
        'What food/drink would you like to remove?\n\n'
        'Please specify full name:\n'
        'Eg: 1 bowl Laksa\n\n'
        'Press /cancel to finish\n'
        )
        text = ""
        find = collection.find({"user" : update.message.chat_id, "date": delete_date})
        for x in find:
            for y in x["item"]:
                text += y["name"] + '\n'
        update.message.reply_text(
            delete_date + ':' + '\n\n' + text
        )
        return DELETEITEM
    except (IndexError, ValueError):
        update.message.reply_text(
            'Please type command in this format\n' +
            'For eg: /removeitem 23/06/2021'
        )
        return ConversationHandler.END

def deleting_item(update: Update, _: CallbackContext):
    global delete_item
    delete_item = str(update.message.text)
    update.message.reply_text(
        'Are you sure to remove ' + delete_item + '?\n\n'
        'Type Yes to remove, No to stop removing'
    )
    return CONFIRMDELETE

def confirm_delete(update: Update, _: CallbackContext):
    reply = str(update.message.text)
    if reply.lower() == "yes":
        log = collection.find_one_and_update(
            {"user": update.message.chat_id , "date": delete_date}, #query
            {'$pull': {"item" : {"name":delete_item}}}, #what to remove db
            upsert = True)
        if log:
            update.message.reply_text(
              'Item has successfully been removed!!'
            )
            return ConversationHandler.END
        else:
            update.message.reply_text(
              'Item was not found, please double check if your input is correct'
            )
            return DELETEITEM
    else:
        update.message.reply_text(
            'What would you like to do next?'
        )
        return ConversationHandler.END
