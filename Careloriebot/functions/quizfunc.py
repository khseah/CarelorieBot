import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

QUIZ_QNS = range(1)

score = 0
num_of_qns = 0
i = random.randint(0,51)
def quiz_start(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        'Are you ready to put your knowledge to the test?\n\n'
        'Send /cancel to stop talking to me.\n',
    )

    reply_keyboard = [['True', 'False', 'Cancel']]
    questions = ["Chronic Diseases can generally be cured",
    "Life expectancy has risen substantially across the world. In 2020, life expectancy was 72.6",
    "Chronic diseases generally start at older ages",
    "Risk factors for chronic diseases are poor diet, lack of physical activity, being overweight, tobacco smoking and harmful use of alcohol",
    "Chronic diseases affect mostly high income countries due to poor diet choices, tobacco smoking and harmful use of alcohol",
    "Chronic diseases are the leading cause of death worldwide, resulting in 40 million deaths each year",
    "Cancer cells, like normal cells, are programmed to \"die\" eventually",
    "Common chronic diseases include heart disease, stroke, cancer, lung disease, diabetes and dementia",
    "There are about 70 types of cancer",
    "Risk for most cancers increases with age",
    "Stomach cancer develops rapidly, however is easily detected as there are outward symptoms",
    "A mass of abnormal cells are known as cancerous tumours. Some tumours are benign",
    "The surgical procedure in which a robot does the surgery is known as robotic surgery",
    "Tobacco smoking is the most significant risk factor for cancer",
    "Type 2 diabetes is hard to prevent or delay even with adopting a healthier lifestyle",
    "In Singapore, colorectal cancer is the most common form of cancer in men",
    "Majority of diabetic patients can still live above 70 years old",
    "Major risk factors for diabetes are poor diet, excess weight, physical inactivity and smoking",
    "Insulin resistance can be easily dectected as symptoms include feeling lethargic and high blood pressure",
    "The greatest risk factor for type 2 diabetes is excess body fat",
    "Amputations arising from diabetes complications are possible but uncommon",
    "Diabetes is the leading cause of blindness, amputation and kidney failure",
    f"More than 75% of cardiovascular disease deaths occur in high-income countries",
    "In type 1 diabetes, the immune system attacks the insulin-producing cells, affecting insulin production by the body",
    "Heart failure is also known as a heart attack",
    "Cardiovascular disease is the largest cause of death globally",
    "Fatty deposits in blood vessels from eating foods high in saturated fat can be removed through proper treatment",
    f"80% of all cardiovascular disease deaths are due to heart attack and stroke",
    "Saturated and trans fat are healthy fats, while mono and polyunsaturated fats are harmful",
    "A Stroke occurs when blood vessels within the brain or an artery carrying blood to the brain is blocked or damaged",
    "Ultrasound imaging is dangerous as it utilizes ionizing radiation to image tissues and structures inside the body",
    "High salt intake is associated with an increased risk of high blood pressure",
    "High density cholesterol increases risks for heart disease and stroke",
    "High blood pressure is the leading risk factor for cardiovascular disease",
    "Men are more likely to develop osteoporosis than women",
    "Osteoporosis is the condition characterized by the loss of density and mass of bone to unhealthy levels",
    "Osteoporosis is easy to detect and diagnose as many symptoms are present in the early stages",
    "Spongy bone consists of a porous network of bone cells and provides a measure of flexibility to bone structure",
    "Calcium supplements and medications can help reverse bone density loss due to osteoporosis",
    "Osteoporosis is the leading cause of hip fractures",
    "Breast cancer is equally likely to occur in both males and females",
    "Breast cancer is the most lethal cancer among women in Singapore",
    "Dementia refers to a single disease which is the degenerative disease of the brain",
    "Mammography is an X-ray projection imaging of the breast",
    "Through proper treatment, Alzheimer's disease can be cured",
    f"Alzheimer's disease is the most common form of dementia, constituting 60% - 80% of all dementia cases",
    "It is uncommon for a dementia patient to suffer from both Alzheimer's and vascular dementia",
    "1 in 10 people over age 65 and more than half of those over 85 have Alzheimer's disease",
    "Dementia is also known as Alzheimer's disease",
    "Vascular dementia is the second most common form of Dementia, caused by an abnormal blood flow to the brain",
    "Thirdhand smoke poses a small health hazard to non smokers",
    "The main risk factor for lung disease is smoking and breathing in of second hand smoke",
    ]

    update.message.reply_text(
        questions[i],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return QUIZ_QNS

def quiz_qns(update: Update, _: CallbackContext) -> int: 
    global num_of_qns
    global score
    global i
    num_of_qns += 1

    ans = update.message.text
    if (ans == 'Cancel'):
        update.message.reply_text(
        'Your score: ' + str(score) + "/" + str(num_of_qns-1), reply_markup=ReplyKeyboardRemove()
        )
        score = 0
        num_of_qns = 0
        return ConversationHandler.END 
    elif ((i % 2 == 0) and (ans == 'False')):
        update.message.reply_text(
        'That\'s right!' + u"\u2705",
        reply_markup=ReplyKeyboardRemove(),
        )
        score += 1
    elif ((i % 2 == 1) and (ans == 'True')):
        update.message.reply_text(
        'That\'s right!' + u"\u2705",
        reply_markup=ReplyKeyboardRemove(),
        )
        score += 1
    else:
        update.message.reply_text(
        'Sorry, that\'s wrong.. Try Again!!',
        reply_markup=ReplyKeyboardRemove(),
        )

    questions = ["Chronic Diseases can generally be cured",
    "Life expectancy has risen substantially across the world. In 2020, life expectancy was 72.6",
    "Chronic diseases generally start at older ages",
    "Risk factors for chronic diseases are poor diet, lack of physical activity, being overweight, tobacco smoking and harmful use of alcohol",
    "Chronic diseases affect mostly high income countries due to poor diet choices, tobacco smoking and harmful use of alcohol",
    "Chronic diseases are the leading cause of death worldwide, resulting in 40 million deaths each year",
    "Cancer cells, like normal cells, are programmed to \"die\" eventually",
    "Common chronic diseases include heart disease, stroke, cancer, lung disease, diabetes and dementia",
    "There are about 70 types of cancer",
    "Risk for most cancers increases with age",
    "Stomach cancer develops rapidly, however is easily detected as there are outward symptoms",
    "A mass of abnormal cells are known as cancerous tumours. Some tumours are benign",
    "The surgical procedure in which a robot does the surgery is known as robotic surgery",
    "Tobacco smoking is the most significant risk factor for cancer",
    "Type 2 diabetes is hard to prevent or delay even with adopting a healthier lifestyle",
    "In Singapore, colorectal cancer is the most common form of cancer in men",
    "Majority of diabetic patients can still live above 70 years old",
    "Major risk factors for diabetes are poor diet, excess weight, physical inactivity and smoking",
    "Insulin resistance can be easily dectected as symptoms include feeling lethargic and high blood pressure",
    "The greatest risk factor for type 2 diabetes is excess body fat",
    "Amputations arising from diabetes complications are possible but uncommon",
    "Diabetes is the leading cause of blindness, amputation and kidney failure",
    f"More than 75% of cardiovascular disease deaths occur in high-income countries",
    "In type 1 diabetes, the immune system attacks the insulin-producing cells, affecting insulin production by the body",
    "Heart failure is also known as a heart attack",
    "Cardiovascular disease is the largest cause of death globally",
    "Fatty deposits in blood vessels from eating foods high in saturated fat can be removed through proper treatment",
    f"80% of all cardiovascular disease deaths are due to heart attack and stroke",
    "Saturated and trans fat are healthy fats, while mono and polyunsaturated fats are harmful",
    "A Stroke occurs when blood vessels within the brain or an artery carrying blood to the brain is blocked or damaged",
    "Ultrasound imaging is dangerous as it utilizes ionizing radiation to image tissues and structures inside the body",
    "High salt intake is associated with an increased risk of high blood pressure",
    "High density cholesterol increases risks for heart disease and stroke",
    "High blood pressure is the leading risk factor for cardiovascular disease",
    "Men are more likely to develop osteoporosis than women",
    "Osteoporosis is the condition characterized by the loss of density and mass of bone to unhealthy levels",
    "Osteoporosis is easy to detect and diagnose as many symptoms are present in the early stages",
    "Spongy bone consists of a porous network of bone cells and provides a measure of flexibility to bone structure",
    "Calcium supplements and medications can help reverse bone density loss due to osteoporosis",
    "Osteoporosis is the leading cause of hip fractures",
    "Breast cancer is equally likely to occur in both males and females",
    "Breast cancer is the most lethal cancer among women in Singapore",
    "Dementia refers to a single disease which is the degenerative disease of the brain",
    "Mammography is an X-ray projection imaging of the breast",
    "Through proper treatment, Alzheimer's disease can be cured",
    f"Alzheimer's disease is the most common form of dementia, constituting 60% - 80% of all dementia cases",
    "It is uncommon for a dementia patient to suffer from both Alzheimer's and vascular dementia",
    "1 in 10 people over age 65 and more than half of those over 85 have Alzheimer's disease",
    "Dementia is also known as Alzheimer's disease",
    "Vascular dementia is the second most common form of Dementia, caused by an abnormal blood flow to the brain",
    "Thirdhand smoke poses a small health hazard to non smokers",
    "The main risk factor for lung disease is smoking and breathing in of second hand smoke",
    ]
    i = random.randint(0,51)
    reply_keyboard = [['True', 'False', 'Cancel']]
    update.message.reply_text(
        questions[i],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )    

    return QUIZ_QNS

def quiz_cancel(update: Update, _: CallbackContext) -> int:
    global score
    global num_of_qns
    update.message.reply_text(
        'Your score: ' + str(score) + "/" + str(num_of_qns), reply_markup=ReplyKeyboardRemove()
    )
    score = 0
    num_of_qns = 0
    return ConversationHandler.END 