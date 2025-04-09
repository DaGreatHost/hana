
import telebot
import openai
import os
import json
import time
import random
import threading
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from vc_lines import vc_lines
from vip_lines import vip_lines
from hana_lines import get_dynamic_line

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_file = "users.json"


flirty_greetings = ['Hoyy 😜 bat ngayon ka lang?', 'Eyy kamusta ka na? Miss mo ko noh? 🤭', 'YO din! Pero mas cute ako 😎', 'Uy! G ka ba sa landian today? 😏', 'Hellooo~ Ready ka na ba sa kulitan natin? 😘']
short_noise_replies = ['Ang lalim ng sinabi mo ah... char 😜', 'Typing pa yan? Parang bitin 😏', 'May gusto ka bang sabihin o nagpaparamdam ka lang? 😚', "Gusto mo 'ko kausapin pero di mo alam pano simulan noh? 🤭", "Grabe 'to, nagpaparamdam gamit lang ng tuldok 😈", 'Ayan na... mysterious reply 😎']

MEDIA_FOLDER = "hana_media/hanapics"

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

# Filter: skip GPT for nonsense/short/generic messages
def is_meaningful(text):
    low = text.strip().lower()
    if len(low) < 4:
        return False
    if low in ["hi", "hello", "ok", "okay", "yes", "no", "haha", "lol", "hm", "hmm", "huhu", "bye", "bai", "yo", "yo!", "oi", "uy", "haha!", "hello!", "hi!"]:
        return False
    if all(char in "👍😂🥺❤️🔥💀💯👌😎😩😳😍😘😏" for char in low):
        return False
    return True

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

# GPT core chat
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

# Detect keyword triggers
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

# Payment button
def payment_keyboard(tag=None):
    markup = InlineKeyboardMarkup()
    if tag == "vc":
        markup.add(InlineKeyboardButton("📹 Video Call ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"))
    elif tag == "vip":
        markup.add(InlineKeyboardButton("💎 VIP Vault ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"))
    else:
        markup.add(InlineKeyboardButton("💎 VIP ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"))
        markup.add(InlineKeyboardButton("📹 Video Call ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"))
    return markup

# Handle messages
@bot.message_handler(func=lambda m: True)
def on_message(message):
    chat_id = message.chat.id
    text = message.text
    username = message.from_user.first_name

    register(chat_id, username)
    user_msg_count[chat_id] = user_msg_count.get(chat_id, 0) + 1

    reply = keyword_reply(text)
    if reply:
        return bot.send_message(chat_id, reply)

    if user_msg_count[chat_id] == 10:
        bot.send_message(chat_id, "Alam mo ba… may mga bagay akong sinasabi lang sa VIP 🤫", reply_markup=payment_keyboard("vip"))
    elif user_msg_count[chat_id] == 15:
        bot.send_message(chat_id, get_dynamic_line("vc_pitch"), reply_markup=payment_keyboard("vc"))


    if not is_meaningful(text):
        # Short but not ignored: give static flirty reply
        if text.lower() in ["hi", "hello", "kamusta", "yo", "oi", "uy"]:
            return bot.send_message(chat_id, random.choice(flirty_greetings))
        if all(char in ".?!~…" for char in text.strip()):
            return bot.send_message(chat_id, random.choice(short_noise_replies))
        return  # Skip silent

    gpt_reply = chat_with_hana(text)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(min(len(gpt_reply.split()) * 0.3, 4))
    bot.send_message(chat_id, gpt_reply)

# Admin command
@bot.message_handler(commands=["getusers"])
def on_get_users(message):
    if message.chat.id == ADMIN_ID:
        with open(users_file, "rb") as f:
            bot.send_document(message.chat.id, f)

# Silent checker for 1hr inactivity (VC pitch)
def silent_check():
    while True:
        now = datetime.now()
        for chat_id_str, data in users.items():
            chat_id = int(chat_id_str)
            last = datetime.fromisoformat(data["last_active"])
            if (now - last) > timedelta(hours=1):
                if chat_id not in last_vc_offer or (now - datetime.fromisoformat(last_vc_offer[chat_id])) > timedelta(hours=1):
                    bot.send_message(chat_id, "Hey, baka gusto mong video call muna tayo… ₱250 lang 👀", reply_markup=payment_keyboard("vc"))
                    last_vc_offer[chat_id] = datetime.now()
        time.sleep(300)

# Auto-send VC media every 30 min
def auto_send_vc():
    while True:
        for chat_id in users.keys():
            try:
                file = random.choice(os.listdir(MEDIA_FOLDER))
                photo_path = os.path.join(MEDIA_FOLDER, file)
                caption = random.choice(vc_lines)
                bot.send_photo(chat_id=int(chat_id), photo=open(photo_path, 'rb'), caption=caption, reply_markup=payment_keyboard("vc"))
            except Exception as e:
                print(f"[VC AutoSend Error]: {e}")
        time.sleep(1800)

# Auto-send VIP media every 1hr
def auto_send_vip():
    while True:
        for chat_id in users.keys():
            try:
                file = random.choice(os.listdir(MEDIA_FOLDER))
                photo_path = os.path.join(MEDIA_FOLDER, file)
                caption = random.choice(vip_lines)
                bot.send_photo(chat_id=int(chat_id), photo=open(photo_path, 'rb'), caption=caption, reply_markup=payment_keyboard("vip"))
            except Exception as e:
                print(f"[VIP AutoSend Error]: {e}")
        time.sleep(3600)

# Launch threads
threading.Thread(target=silent_check, daemon=True).start()
threading.Thread(target=auto_send_vc, daemon=True).start()
threading.Thread(target=auto_send_vip, daemon=True).start()

bot.infinity_polling()
