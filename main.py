
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
from trigger_lines import vc_triggers, vc_replies, booking_triggers, booking_replies

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_file = "users.json"
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
    if low in ["hi", "hello", "ok", "okay", "yes", "no", "haha", "lol", "hm", "hmm", "huhu", "bye", "bai", "yo", "yo!", "oi", "uy", "haha!", "hello!", "hi!"]:
        return False
    if all(char in "👍😂🥺❤️🔥💀💯👌😎😩😳😍😘😏" for char in low):
        return False
    return True

def static_reply_for_nonsense(text):
    lowered = text.strip().lower()
    greeting_replies = [
        "Hoyyy 😜 ngayon ka lang?",
        "Eyy kamusta ka na? Miss mo ko noh? 🤭",
        "YO din! Pero mas hot ako 😎",
        "Uy! G ka ba sa landian today? 😏",
        "Hellooo~ Ready ka na ba sa kulitan natin? 😘"
    ]
    noise_replies = [
        "Ang lalim ng sinabi mo ah... char 😜",
        "Typing pa yan? Parang bitin 😏",
        "May gusto ka bang sabihin o nagpaparamdam ka lang? 😚",
        "Gusto mo 'ko kausapin pero di mo alam pano simulan noh? 🤭",
        "Grabe 'to, nagpaparamdam gamit lang ng tuldok 😈"
    ]
    if lowered in ["hi", "hello", "kamusta", "kumusta", "yo", "uy", "oi"]:
        return random.choice(greeting_replies)
    if all(char in ".?!~…" for char in lowered):
        return random.choice(noise_replies)
    return None

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


@bot.message_handler(commands=["getusers"])
def on_get_users(message):
    if message.chat.id == ADMIN_ID:
        with open(users_file, "rb") as f:
            bot.send_document(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, "❌ Not allowed. This command is for admin only.")


@bot.message_handler(func=lambda m: True)
def on_message(message):
    chat_id = message.chat.id
    text = message.text
    username = message.from_user.first_name

    register(chat_id, username)
    user_msg_count[chat_id] = user_msg_count.get(chat_id, 0) + 1


    # Triggered replies
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

    reply = keyword_reply(text)
    if reply:
        return bot.send_message(chat_id, reply)

    if user_msg_count[chat_id] == 10:
        bot.send_message(chat_id, "Alam mo ba… may mga bagay akong sinasabi lang sa VIP 🤫", reply_markup=payment_keyboard("vip"))
    elif user_msg_count[chat_id] == 15:
        bot.send_message(chat_id, get_dynamic_line("vc_pitch"), reply_markup=payment_keyboard("vc"))

    if not is_meaningful(text):
        reply = static_reply_for_nonsense(text)
        if reply:
            return bot.send_message(chat_id, reply)
        return

    gpt_reply = chat_with_hana(text)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(min(len(gpt_reply.split()) * 0.25, 4))
    bot.send_message(chat_id, gpt_reply)

@bot.message_handler(commands=["getusers"])
def on_get_users(message):
    if message.chat.id == ADMIN_ID:
        with open(users_file, "rb") as f:
            bot.send_document(message.chat.id, f)

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

threading.Thread(target=silent_check, daemon=True).start()
threading.Thread(target=auto_send_vc, daemon=True).start()
threading.Thread(target=auto_send_vip, daemon=True).start()

bot.infinity_polling()
