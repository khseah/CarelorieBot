import logging
import requests
import random

# Set your bot_token here
bot_token = "1892475607:AAFvbstR9Sg2I99rdg36DpLHl5YHOF-Gp-w"

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

HEIGHT, WEIGHT, FOOD = range(3)

# Functions to handle each command
def start(update, context):
    name = update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi " + name +", welcome to Careloriebot, a one stop platform to resolve your fitness needs.")

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
    response = requests.get(endpoint + query, headers={'X-Api-Key': 'v3IAHHkuhZBm+0jirF9mXg==XhBrVYmOSZqG3kD9'})
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

def healthfacts(update, context):
    facts = ["Chronic diseases are the leading cause of death worldwide, resulting in 40 million deaths each year",
    "80% of deaths due to chronic diseases occur in low income countries",
    "Chronic diseases are long term, generally incurable illness that affects a person's daily life and require ongoing medical attention",
    "Common chronic diseases are heart disease, stroke, cancer, arthritis, lung disease, diabetes, dementia etc",
    "Life expectancy has risen substantially across the world. In 2020, life expectancy was 72.6",
    "Risk factors for chronic diseases are poor diet, lack of physical activity, being overweight, tobacco smoking and harmful use of alcohol",
    "Chronic diseases are incurable. The best way to deal with them is prevention or to control the symptoms and slow down the progression",
    "Chronic diseases usually take a long time to develop. They have their origin at young ages",
    "If improperly managed, chronic diseases will have a snowballing effect, resulting in people suffering from more than 1 condition at the same time",
    "Medical technology is used for health screening for delay of onset, early detection and improved treatment for chronic diseases",
    "Chronic diseases have reached epidemic levels worldwide",
    "DNA consists of 2 strands twisted in a double helix structure and is further coiled into chromosomes",
    "Total length of DNA strands in a single cell is approximately 2 meters",
    "DNA strands undergo multiple orders of coiling and is packed into 23 pairs of chromosomes",
    "There are about 20,000 genes in a typical cell within the human body",
    "A gene is a segment of DNA which contains information on how to produce a specific protein",
    "The complete collection of information stored in the entire DNA is called the genome",
    "At the end of their life cycle, cells are programmed to die. This process is known as apoptosis",
    "Unlike normal cells, cancer cells do not \"die\". They continue to grow and divide out of control",
    "A mass of abnormal cells are known as cancerous tumours. Some tumours are benign",
    "Risk for most cancers increases with age",
    "Nearly all cancers are caused by abnormalities in DNA due to effects of carcinogens, ionizing radiation or are inherited",
    "During advanced stages of cancer, metastasis may occur, where cancer cells from tumours spread to other parts of the body and start new tumours",
    "Cancer causes about 14% of all deaths worldwide. There were 9.6 million cancer deaths globally in 2018",
    "There are over 100 types of cancer",
    "Tobacco smoking is the most significant risk factor for cancer",
    "Colorectal cancer is the cancer of colon and rectum, and is the third most common cancer globally",
    "In Singapore, colorectal cancer is the most common form of cancer in men",
    "Everyday, 5 people in Singapore are diagnosed with colorectal cancer and 2 die from it",
    "Stomach cancer is the leading cancer type in Korea for men aged 35-64 years",
    "Stomach cancers tend to develop slowly over many years and early stages often go undetected as there are no outward symptoms",
    "Diets containing large amounts of smoked foods, pickled vegetables and cured meats are shown to increase the risk of stomach cancer",
    "Fruits and vegetables have shown to decrease the risk of stomach cancer",
    "Colonscopy is the procedure of using an endoscope to look at the interior of the rectum and colon",
    "Keyhole surgery is a surgical technique in which operations are performed through small incisions",
    "Colectomy is the process of removing part of the colon containing the tumour and stitching the remaining healthy sections together",
    "Diabetes refers to a family of diseases that result in the blood sugar level to be consistently too high",
    "Diabetes is the 7th leading cause of death in the United States",
    "43% of all deaths due to diabetes occur prematurely, before the age of 70",
    "In Singapore, there are roughly 3 amputations per day due to complications arising from diabetes",
    "Insulin is a hormone that allows cells to absorb glucose in the blood and use it as an energy source",
    "Insulin acts to regulate glucose level in the blood",
    "Insulin resistance occurs when body cells are unable to readily absorb glucose from the bloodstream",
    "Insulin resistance has no obvious symptoms in many cases",
    "Major risk factors for diabetes are poor diet, excess weight, physical inactivity and smoking",
    "In type 1 diabetes, the immune system attacks the insulin-producing cells, affecting insulin production by the body",
    "Type 2 diabetes is caused when the body can no longer effectively use insulin to regulate glucose level in the blood",
    "The greatest risk factor for type 2 diabetes is excess body fat",
    "High intake of saturated fat and sugar-sweetened beverages has shown to increase risk of diabetes",
    "More than 80% of type 2 diabetes can be prevented or delayed by adopting healthier lifestyles",
    "Diabetes is the leading cause of blindness, amputation and kidney failure",
    "The Cornea is the front window of the eye which transmits and focuses light into the eye",
    "The Iris is the coloured part of the eye which helps regulate the amount of light that enters the eye",
    "The Pupil is the dark center in the middle of the Iris which determines how much light is let into the eye",
    "Vitreous Humour is a jelly-like substance that fills the middle of the eye and maintains the shape of the eye",
    "The Retina is the nerve layer at the back of the eye which senses light and create impulses that are sent to the brain",
    "Diabetic Retinopathy occurs when blood vessels in the eye is damaged by high blood sugar levels, leading to swelling or blood leakage",
    "Glaucoma refers to a group of diseases that damage the optic nerves in the eye",
    "Cataracts refer to the condition where the lens of the eye becomes clouded or when the lens gradually change to a yellow/brown colour",
    "Cardiovascular diseases are a family of diseases involving the heart and blood vessels",
    "Coronary heart disease is the disease of blood vessels leading to the heart",
    "Cerebrovascular disease is the disease of blood vessels leading to or within the brain",
    "Congenital heart disease refers to the malformation of heart structures from birth",
    "Cardiovascular disease is the largest cause of death globally",
    "High blood pressure is the leading risk factor for cardiovascular disease",
    "80% of all cardiovascular disease deaths are due to heart attack and stroke",
    "More than 75% of cardiovascular disease deaths occur in low-income and middle-income countries",
    "Atherosclerosis is the condition where blood vessels harden or constrict due to buildup of fatty deposits on the inner walls",
    "Atherosclerosis begins early in life and progresses gradually, and usually does not cause symptoms at the early stages",
    "No treatment can stop or significantly reverse the process of Atherosclerosis",
    "Angina is the condition where there is pain or discomfort in the chest and is a symptom of heart disease",
    "A Stroke occurs when blood vessels within the brain or an artery carrying blood to the brain is blocked or damaged",
    "High intake of saturated and trans fat has been shown to raise cholesterol levels, increasing the risk of cardiovascular disease",
    "High salt intake is associated with an increased risk of high blood pressure",
    "Replacing saturated and trans fat with mono and poly-unsaturated fat is effective in reducing cardiovascular disease risk",
    "Echocardiography is the ultrasound imaging of the heart",
    "Ultrasound imaging is extremely safe and can be used to monitor development of fetuses",
    "Osteoporosis is the condition characterized by the loss of density and mass of bone to unhealthy levels",
    "Women are 4 times more likely to develop osteoporosis than men",
    "Compact bone forms the outermost layer of most bones and is extremely dense and rigid, providing strength and support",
    "Spongy bone consists of a porous network of bone cells and provides a measure of flexibility to bone structure",
    "Osteoporosis usually has no symptoms and in many cases is only diagnosed when a bone fracture has occured",
    "There is no treatment that can completely reverse bone density loss",
    "Osteoporosis causes more than 8.9 million fractures worldwide",
    "The spine consists of a column of individual bone pieces called vertebrae, separated by shock absorption pads known as intervetebral discs",
    "Osteoporosis is the leading cause of hip fractures",
    "75% of all hip fractures are sustained by women",
    "Breast cancer is the most common cancer in Singapore women, with 1 in 14 contracting breast cancer before age 75",
    "Breast cancer is the most lethal cancer among women in Singapore",
    "Mammography is an X-ray projection imaging of the breast",
    "Dementia is caused by a group of diseases which include Alzheimer's, traumatic brain injury, Down's syndrome etc",
    "Alzheimer's disease is a degenerative disease of the brain, progressing from mild forgetfulness to widespread neurological impairment",
    "Alzheimer's disease is the most common form of dementia, constituting 60% - 80% of all dementia cases",
    "1 in 10 people over age 65 and more than half of those over 85 have Alzheimer's disease",
    "There is currently no cure for Alzheimer's disease",
    "Vascular dementia is the second most common form of Dementia, caused by an abnormal blood flow to the brain",
    "It is common for a dementia patient to suffer from both Alzheimer's and vascular dementia. This is known as mixed dementia",
    "There is currently no treatment available for vascular dementia",
    "Chronic lung disease is a group of diseases that causes reduced airflow capability of the lungs due to obstruction in the airways",
    "The main risk factor for lung disease is smoking and breathing in of second hand smoke",
    "Chronic lung disease is currently the fourth leading cause of death in the world and is predicted to rise to the third leading cause by 2030",
    ]
 
    n = random.randint(0,100)
    update.message.reply_text(
        u"\U0001F4A1" + 'Did you know??' + u"\U0001F4A1"  + '\n\n' + facts[n]
    )
    #context.bot.send_message(chat_id=update.effective_chat.id, text=facts[n])
    

def bmi(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'What is your height in cm?\n\n'
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
            'What is your height in cm?\n'
        )   
        return HEIGHT 
    height_input = height_input/100    
    update.message.reply_text('What is your weight in kg?')
    return WEIGHT

def weight(update: Update, _: CallbackContext) -> int:
    global weight_input 
    weight_status = ""
    try:
        weight_input = int(update.message.text)
    except ValueError:
        update.message.reply_text(
            'That is an invalid input!\n'
            'What is your weight in kg?\n'
        )   
        return WEIGHT 
    bmi = weight_input / (height_input*height_input)
    bmi_str = "{:.2f}".format(bmi)
    if bmi < 18.50 :
        weight_status = 'Your weight status is: Underweight'
    elif 18.50 <= bmi < 25.00:
        weight_status = 'Your weight status is: Normal or Healthy Weight'
    elif 25.00 <= bmi < 30.00:
        weight_status = 'Your weight status is: Overweight'
    else: 
        weight_status = 'Your weight status is: Obese'
    update.message.reply_text(
        'Your BMI is: ' + bmi_str + '\n' + weight_status
    )
    
    return ConversationHandler.END
    
def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Cancelled!\nWhat would you like to find out next?', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Create and add command handlers
def main() -> None:
    # Setting up their polling stuff
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start) #command handler for /start
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help) #command handler for /help
    dispatcher.add_handler(help_handler)
    
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

    fact_handler = CommandHandler('healthfacts', healthfacts)
    dispatcher.add_handler(fact_handler)


    updater.start_polling()
    updater.idle() # ensuress that there wont be any clashes

if __name__ == '__main__':
    main()