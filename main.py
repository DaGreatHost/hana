
import telebot
import openai
import os
import json
import time
import random
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hana_lines import get_dynamic_line

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_file = "users.json"

def load_users():
    try:
        with open(users_file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(users_file, "w") as f:
        json.dump(data, f, indent=2)

users = load_users()
user_msg_count = {}
last_vc_offer = {}

# Payment button
def payment_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💎 VIP ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"))
    markup.add(InlineKeyboardButton("📹 Video Call ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"))
    return markup

# Register user
def register(chat_id, username):
    if str(chat_id) not in users:
        users[str(chat_id)] = {
            "username": username,
            "first_seen": str(datetime.now()),
            "last_active": str(datetime.now())
        }
    else:
        users[str(chat_id)]["last_active"] = str(datetime.now())
    save_users(users)

# GPT + system prompt
def chat_with_hana(user_input):
    with open("hana_prompt.txt", "r") as f:
        system_prompt = f.read()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    res = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return res.choices[0].message.content.strip()

# Detect keywords (defensive + contextual reply triggers)
def keyword_reply(text):
    lowered = text.lower()
    if any(word in lowered for word in ["ai", "bot", "chatgpt"]):
        return "Bot daw ako? Gagi ka 😂 real enough to make you blush ha."
    if "gutom" in lowered:
        return "Ako rin eh… pero iba yata ‘yung gutom ko rn 😈"
    if "tulog" in lowered:
        return "Kung katabi mo lang ako, hindi ka makakatulog promise 😘"
    if "miss" in lowered:
        return get_dynamic_line("sweet")
    return None

# Handle messages
@bot.message_handler(func=lambda m: True)
def on_message(message):
    chat_id = message.chat.id
    text = message.text
    username = message.from_user.first_name

    register(chat_id, username)

    # Count messages
    user_msg_count[chat_id] = user_msg_count.get(chat_id, 0) + 1

    # Check for keyword replies
    reply = keyword_reply(text)
    if reply:
        return bot.send_message(chat_id, reply)

    # Trigger VC and VIP offers
    if user_msg_count[chat_id] == 10:
        bot.send_message(chat_id, "Alam mo ba… may mga bagay akong sinasabi lang sa VIP 🤫", reply_markup=payment_keyboard())
    elif user_msg_count[chat_id] == 15:
        bot.send_message(chat_id, get_dynamic_line("vc_pitch"), reply_markup=payment_keyboard())

    # GPT fallback
    gpt_reply = chat_with_hana(text)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(min(len(gpt_reply.split()) * 0.3, 4))
    bot.send_message(chat_id, gpt_reply)

# Admin: Download user data
@bot.message_handler(commands=["getusers"])
def on_get_users(message):
    if message.chat.id == ADMIN_ID:
        with open(users_file, "rb") as f:
            bot.send_document(message.chat.id, f)

# Background thread to offer VC after 1 hour of silence
import threading
def silent_check():
    while True:
        now = datetime.now()
        for chat_id_str, data in users.items():
            chat_id = int(chat_id_str)
            last = datetime.fromisoformat(data["last_active"])
            if (now - last) > timedelta(hours=1):
                if chat_id not in last_vc_offer or (now - datetime.fromisoformat(last_vc_offer[chat_id])) > timedelta(hours=1):
                    bot.send_message(chat_id, "Hey, baka gusto mong video call muna tayo… ₱250 lang 👀", reply_markup=payment_keyboard())
                    last_vc_offer[chat_id] = now
        time.sleep(300)

threading.Thread(target=silent_check, daemon=True).start()

# Start bot
bot.infinity_polling()
