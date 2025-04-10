import telebot
import openai
import os
import json
import time
import random
import threading
from datetime import datetime, timedelta
from langdetect import detect
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from vc_lines import vc_lines
from vip_lines import vip_lines
from hana_lines import get_dynamic_line
from trigger_lines import vc_triggers, vc_replies, booking_triggers, booking_replies, atabs_triggers

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_file = "users.json"
log_file = "log.json"
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

def is_meaningful(text):
    low = text.strip().lower()
    if len(low) < 4:
        return False
    if low in ["hi", "hello", "kamusta", "kumusta", "yo", "uy", "oi"]:
        return False
    if all(char in "👍😂🥺❤️🔥💀💯👌😎😩😳😍😘😏" for char in low):
        return False
    return True

def static_reply_for_nonsense(text):
    lowered = text.strip().lower()
    greeting_replies = [
        "Heyyy! 😚 Kamusta ka na?",
        "Uy! Ready ka na bang kiligin? 😜",
        "Nandito lang ako ha, waiting sa landi mo 😘",
        "Bati ka lang nang bati ha 😏 Gusto mo talaga makipagkulitan!"
    ]
    noise_replies = [
        "Tuldok lang? Pero bakit parang gusto mong mapansin 😏",
        "Bitin yan... dagdagan mo pa 😚",
        "Dami mong sinabi ah... joke lang, wala pala 🤣",
        "Grabe ka, nagpaparamdam ka lang gamit emoji? 😈"
    ]
    if lowered in ["hi", "hello", "kamusta", "kumusta", "yo", "uy", "oi"]:
        return random.choice(greeting_replies)
    if all(char in ".?!~…" for char in lowered):
        return random.choice(noise_replies)
    return None

def payment_keyboard(tag=None):
    markup = InlineKeyboardMarkup()
    if tag == "vc":
        markup.add(
            InlineKeyboardButton("📹 VC ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"),
            InlineKeyboardButton("💠 Pay via TON", url="https://app.tonkeeper.com/transfer/UQAwroBrBTSzzVYx_IXpR-R_KJ_mZQgmT7uNsUZdJ5MM68ep?amount=2099700000&text=VC_Hana")
        )
    elif tag == "vip":
        markup.add(
            InlineKeyboardButton("💎 VIP ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"),
            InlineKeyboardButton("💠 TON Payment", url="https://app.tonkeeper.com/transfer/UQAwroBrBTSzzVYx_IXpR-R_KJ_mZQgmT7uNsUZdJ5MM68ep?amount=4990000000&text=VIP_Hana")
        )
    else:
        markup.add(InlineKeyboardButton("💎 VIP ₱499", url="https://t.me/Scan2payv1bot?startapp=pay"))
        markup.add(InlineKeyboardButton("📹 VC ₱250", url="https://t.me/Scan2payv1bot?startapp=pay"))
        markup.add(InlineKeyboardButton("💠 Pay via TON", url="https://app.tonkeeper.com/transfer/UQAwroBrBTSzzVYx_IXpR-R_KJ_mZQgmT7uNsUZdJ5MM68ep?text=hana"))
    return markup

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

@bot.message_handler(commands=["totalusers"])
def get_total_users(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"📊 Total users: {len(users)}")

@bot.message_handler(commands=["getusers"])
def on_get_users(message):
    if message.chat.id == ADMIN_ID:
        with open(users_file, "rb") as f:
            bot.send_document(message.chat.id, f)

@bot.message_handler(func=lambda m: True)
def on_message(message):
    chat_id = message.chat.id
    text = message.text
    username = message.from_user.first_name
    now = time.time()

    if str(chat_id) not in users:
        users[str(chat_id)] = {"username": username, "reply_count": 0, "last_active": now}
    else:
        if now - users[str(chat_id)]["last_active"] >= 86400:
            users[str(chat_id)]["reply_count"] = 0
        users[str(chat_id)]["last_active"] = now
    save_users(users)

    # Log user
    log = {}
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log = json.load(f)
    log[str(chat_id)] = {"username": username, "last": text, "at": str(datetime.now())}
    with open(log_file, "w") as f:
        json.dump(log, f, indent=2)

    # Always allow triggers
    for word in text.lower().split():
        if word in vc_triggers:
            file = random.choice(os.listdir(MEDIA_FOLDER))
            photo_path = os.path.join(MEDIA_FOLDER, file)
            caption = random.choice(vc_replies)
            return bot.send_photo(chat_id, photo=open(photo_path, 'rb'), caption=caption, reply_markup=payment_keyboard("vc"))
        if word in booking_triggers:
            msg = random.choice(booking_replies)
            btn = InlineKeyboardMarkup()
            btn.add(InlineKeyboardButton("📍 Book Me Now", url="https://t.me/yourpinayatabs_bot?startapp=Login"))
            return bot.send_message(chat_id, msg, reply_markup=btn)
    if word in atabs_triggers:
        msg = "Gusto mo ng trending ATABS content? 📲 Check this out:",
               "Gusto mo ng trending ATABS content? 📲 Check this out:",
                "Hanap mo ba ng Pinay Tabs na wild? 😈 Ito yung vault:",
                "Ito ‘yung hinahanap mong trending ATABS 🔥 Saktong pampainit:",
                "Wag na maghanap sa iba… eto na ‘yung legit tabs vault 😏",
                "Pinayatabs addict ka rin? Same tayo 🤭 Eto na link baby:"
        btn = InlineKeyboardMarkup()
        btn.add(InlineKeyboardButton("🔗 View ATABS Vault", url="https://t.me/trendsmodbot"))
        return bot.send_message(chat_id, msg, reply_markup=btn)


    if users[str(chat_id)]["reply_count"] >= 5:
        bot.send_message(chat_id, "Later nalang pag nag avail kana sir 😌")
        return

    if not is_meaningful(text):
        reply = static_reply_for_nonsense(text)
        if reply:
            bot.send_message(chat_id, reply)
            users[str(chat_id)]["reply_count"] += 1
            save_users(users)
        return

    reply = chat_with_hana(text)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(min(len(reply.split()) * 0.25, 4))
    bot.send_message(chat_id, reply)
    users[str(chat_id)]["reply_count"] += 1
    save_users(users)

def auto_send_vc():
    while True:
        for chat_id in users.keys():
            try:
                file = random.choice(os.listdir(MEDIA_FOLDER))
                photo_path = os.path.join(MEDIA_FOLDER, file)
                caption = random.choice(vc_lines)
                bot.send_photo(chat_id=int(chat_id), photo=open(photo_path, 'rb'), caption=caption, reply_markup=payment_keyboard("vc"))
            except: continue
        time.sleep(1800)

def auto_send_vip():
    while True:
        for chat_id in users.keys():
            try:
                file = random.choice(os.listdir(MEDIA_FOLDER))
                photo_path = os.path.join(MEDIA_FOLDER, file)
                caption = random.choice(vip_lines)
                bot.send_photo(chat_id=int(chat_id), photo=open(photo_path, 'rb'), caption=caption, reply_markup=payment_keyboard("vip"))
            except: continue
        time.sleep(3600)

threading.Thread(target=auto_send_vc, daemon=True).start()
threading.Thread(target=auto_send_vip, daemon=True).start()

bot.infinity_polling()
