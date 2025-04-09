
# main.py — Hana Enhanced Bot with Soul
import telebot
import openai
import os
import json
import random
import time
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hana_lines import (
    get_random_line,
    get_deep_thought,
    get_late_night_thought,
    get_soft_whisper,
    get_silent_reply,
    get_secret_confession
)

# Env variables
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Load and save user data
USER_FILE = "users.json"
def load_user_data():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(USER_FILE, "w") as file:
        json.dump(data, file, indent=4)

users = load_user_data()
user_interactions = {}
last_video_pitch = {}
user_moods = {}

# Payment Buttons
def payment_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 VIP ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"))
    markup.add(InlineKeyboardButton("📹 Video Call ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"))
    return markup

# Memory & register
def register_user(chat_id, username):
    now = str(datetime.now())
    if str(chat_id) not in users:
        users[str(chat_id)] = {
            "username": username,
            "first_interaction": now,
            "last_active": now,
            "messages": 0,
            "mood": "default"
        }
    else:
        users[str(chat_id)]["last_active"] = now
        users[str(chat_id)]["username"] = username
    users[str(chat_id)]["messages"] += 1
    save_user_data(users)

# AI Chat with Hana
def chat_with_hana(user_message, username):
    with open("hana_prompt.txt", "r") as f:
        prompt = f.read()

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message}
    ]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# Typing delay simulation
def send_typing_and_reply(chat_id, reply):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(min(len(reply.split()) * 0.3, 5))
    bot.send_message(chat_id, reply)

# Main handler
@bot.message_handler(content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    username = message.from_user.first_name
    register_user(chat_id, username)

    text = message.text.lower()
    users[str(chat_id)]["mood"] = users[str(chat_id)].get("mood", "default")
    mood = users[str(chat_id)]["mood"]

    # Mood command triggers
    if text == "/lambing":
        users[str(chat_id)]["mood"] = "clingy"
        return bot.reply_to(message, "Lambing mode activated 🥺")
    elif text == "/wild":
        users[str(chat_id)]["mood"] = "naughty"
        return bot.reply_to(message, "Wild Hana unlocked 😈")
    elif text == "/selosa":
        users[str(chat_id)]["mood"] = "selosa"
        return bot.reply_to(message, "Hmm... selosa mood on 😤")

    # Keyword triggers
    if any(word in text for word in ["tulog", "sleep"]):
        return send_typing_and_reply(chat_id, "Kung katabi mo lang ako, baka hindi ka na makatulog 😚")
    elif "cute" in text:
        return send_typing_and_reply(chat_id, "Ikaw rin ah... wag kang ganyan baka ma-fall ako 😳")

    # Time-based soul responses
    hour = datetime.now().hour
    if 23 <= hour or hour < 2:
        if random.random() < 0.3:
            return send_typing_and_reply(chat_id, get_late_night_thought())

    # Random soul behavior
    rand = random.random()
    if rand < 0.05:
        return send_typing_and_reply(chat_id, get_soft_whisper())
    elif 0.05 <= rand < 0.08:
        return send_typing_and_reply(chat_id, get_deep_thought())
    elif 0.08 <= rand < 0.1:
        return send_typing_and_reply(chat_id, get_silent_reply())
    elif 0.1 <= rand < 0.12 and users[str(chat_id)]["messages"] > 30:
        return send_typing_and_reply(chat_id, get_secret_confession())

    # Mood-based variation
    if mood == "clingy":
        response = get_random_line("clingy")
    elif mood == "naughty":
        response = get_random_line("naughty")
    else:
        response = chat_with_hana(message.text, username)

    send_typing_and_reply(chat_id, response)

    count = users[str(chat_id)]["messages"]
    if count == 10:
        send_typing_and_reply(chat_id, "Alam mo ba... may mga bagay akong sinasabi lang sa VIP 🤫 Interested?")
        bot.send_message(chat_id, "G ka?", reply_markup=payment_keyboard())
    elif count == 15:
        send_typing_and_reply(chat_id, "May video call option ako... but only if kaya mong handle-in ‘yung real me 😏 ₱250 lang oh.")
        bot.send_message(chat_id, "Tap here to unlock 💋", reply_markup=payment_keyboard())

# Admin: Download user file
@bot.message_handler(commands=['getusers'])
def get_users_file(message):
    if message.chat.id == ADMIN_ID:
        with open(USER_FILE, "rb") as f:
            bot.send_document(message.chat.id, f)

# Scheduled 1hr silence checker
import threading

def check_silent_users():
    while True:
        now = datetime.now()
        for chat_id_str, data in users.items():
            chat_id = int(chat_id_str)
            last_active = datetime.fromisoformat(data["last_active"])
            if now - last_active >= timedelta(hours=1):
                if chat_id not in last_video_pitch or now - datetime.fromisoformat(last_video_pitch[chat_id]) > timedelta(hours=1):
                    send_typing_and_reply(chat_id, "Hey, wala ka na ba? Baka naman gusto mong video call muna tayo, ₱250 lang… kung ready ka na talaga sa real me 😘")
                    bot.send_message(chat_id, "Tap here to unlock 💋", reply_markup=payment_keyboard())
                    last_video_pitch[chat_id] = now
        time.sleep(300)

threading.Thread(target=check_silent_users, daemon=True).start()

# Run the bot
bot.infinity_polling()
