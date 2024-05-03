import json
import os
import requests
import redis
from telebot import types, TeleBot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize your Telegram bot
bot = TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))

# Connect to Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD")
)

# Global variables
chat_id = {}
log_key = 0

# Function to add user data to Redis
def add_user_data(id, category, username):
    users_data = redis_client.get("users_data")
    if users_data:
        users_data = json.loads(users_data)
    else:
        users_data = []

    existing_user = next((player for player in users_data if player["id"] == id), None)

    if existing_user is not None:
        existing_user["category"] = category
        existing_user["username"] = username
    else:
        new_user = {"id": id, "category": category, "chance_count": 0, "username": username}
        users_data.append(new_user)

    redis_client.setex("users_data", 86400, json.dumps(users_data))

# Command handler for '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    library = types.KeyboardButton('Library')
    social = types.KeyboardButton('Social Media Links')
    keyboard.add(library, social)

    global log_key
    log_key = 3

    if message.chat.first_name and message.chat.last_name:
        greeting = f'Hello! {message.chat.first_name} {message.chat.last_name}, Welcome From Conceptians!'
    elif message.chat.first_name:
        greeting = f'Hello! {message.chat.first_name}, Welcome From Conceptians!'
    else:
        greeting = 'Hello! Welcome From Conceptians!'

    bot.send_message(message.chat.id, greeting, reply_markup=keyboard)

# Command handler for 'Library'
@bot.message_handler(func=lambda message: message.text == 'Library')
def library(message):
    url = "https://v1.conceptians.org/bot"
    headers = {"Authorization": f"Bearer {os.getenv('CONCEPTIANS_API_KEY')}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)

        for category in data:
            button = types.KeyboardButton(category['category'])
            keyboard.add(button)

        global log_key
        log_key = 1
        bot.send_message(message.chat.id, 'Choose Categories that you want to read', reply_markup=keyboard)

    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        bot.send_message(message.chat.id, "An error occurred while fetching data.")

# Message handler for selected category
@bot.message_handler(func=lambda message: True if log_key == 1 else False)
def books(message):
    add_user_data(message.chat.id, message.text, message.chat.username)

    keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    button = types.KeyboardButton("Library")
    keyboard.add(button)

    url = f"https://v1.conceptians.org/bot/{message.text}"

    try:
        response = requests.get(url, headers={"Authorization": f"Bearer {os.getenv('CONCEPTIANS_API_KEY')}"})
        response.raise_for_status()
        json_data = response.json()

        for data in json_data:
            button = types.KeyboardButton(data['title'])
            keyboard.add(button)

        global log_key
        log_key = 2
        bot.send_message(message.chat.id, 'Choose Books that you want to download', reply_markup=keyboard)

    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        bot.send_message(message.chat.id, "An error occurred while fetching data.")

# Message handler for downloading books
@bot.message_handler(func=lambda message: True if log_key == 2 else False)
def download_books(message):
    users_data = redis_client.get("users_data")

    if users_data:
        users_data = json.loads(users_data)
    else:
        users_data = []

    for user in users_data:
        if user["id"] == message.chat.id:
            url = f"https://v1.conceptians.org/bot/{user['category']}"

            try:
                response = requests.get(url, headers={"Authorization": f"Bearer {os.getenv('CONCEPTIANS_API_KEY')}"})
                response.raise_for_status()
                json_data = response.json()

                for book in json_data:
                    if book['title'].replace(" ", "") == message.text.replace(" ", ""):
                        title = f"<b>{book['title']}</b>"
                        cat = f"<i>Category: {book['category']}</i>"
                        filesize = f"<i>File size: {book['filesize']}mb</i>"
                        download = book['link']
                        button = types.InlineKeyboardButton(text='Download', url=download)
                        keyboard = types.InlineKeyboardMarkup([[button]])

                        try:
                            photo_url = book['image']
                            bot.send_photo(chat_id=message.chat.id, photo=photo_url)
                        except:
                            print('no photo')

                        bot.send_message(message.chat.id, f"{title}\n{cat}\n{filesize}", parse_mode='HTML',
                                         reply_markup=keyboard)

                        return

            except requests.RequestException as e:
                print(f"Error making API request: {e}")
                bot.send_message(message.chat.id, "An error occurred while fetching data.")

    bot.send_message(message.chat.id, "No book found for the user ID.")
    

# Command handler for 'Social Media Links'
@bot.message_handler(func=lambda message: message.text == 'Social Media Links')
def social_media_links(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        text='Facebook',
        url='https://www.facebook.com/profile.php?id=100082812927163')
    button2 = types.InlineKeyboardButton(
        text='Youtube', 
        url='https://www.youtube.com/@conceptians8961/featured')
    button3 = types.InlineKeyboardButton(
        text='Instagram', 
        url='https://www.instagram.com/conceptians_org')
    button4 = types.InlineKeyboardButton(
        text='Linkedin', 
        url='https://www.linkedin.com/company/conceptians/')
    button5 = types.InlineKeyboardButton(
        text='Tiktok', 
        url='https://www.tiktok.com/@conceptians')
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    keyboard.add(button5)

    bot.send_message(message.chat.id, "Click the button to open the link:", reply_markup=keyboard)

# Start the bot polling
bot.polling()
