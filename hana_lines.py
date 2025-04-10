import random

def get_random_landi():
    lines = [
        "Bakit parang gusto mong hawakan kita sa hindi dapat? 😈",
        "Kung andito lang ako, baka di mo kayanin ‘yung gagawin ko sayo rn 😏",
        "Pwede bang ako naman ang utusan mo... habang nakabukaka ako? 😘",
        "Sige nga, pa-imagine ng kamay mo sa legs ko habang hinihimas ko sarili ko.",
        "Sarap ng usapan natin… pero mas masarap siguro kung VC na 😳",
        "Ang libog mo tignan habang tahimik ka. Gusto mo ba ‘kong tikman? 😩",
        "Kung ‘tong kamay ko nasa loob na ng panty ko, anong gusto mong gawin ko next?",
        "Sabihin mo lang kung anong gusto mo… baka gawin ko on cam 👀",
        "Naka-panty lang ako ngayon habang nagta-type. Tinatanggal ko na oh…",
        "Bakit parang gusto mong i-VC ko ‘yung ginagawa ko ngayon? 😘",
        "Imaginin mong dinidilaan ko leeg mo habang pinipisil kita dahan-dahan.",
        "Gusto mo bang isubo ko pangalan mo habang umiiyak sa sarap? 🤤",
        "Aaminin ko… basang-basa na ‘ko habang iniisip ka.",
        "‘Wag mo kong subukan kung di mo kaya dalhin ‘yung libog ko.",
        "Halika na… VC tayo. Uutusan mo ko habang naka-finger ako 😈",
    ]
    return random.choice(lines)


def get_greeting_reply():
    lines = [
        "Hi din 😘 pero mas gusto ko ‘yung may landi agad 👀",
        "Hello… anong balak mo sakin? 😈",
        "Kamusta? Pwede ba kitang pasayahin ngayong gabi? 😏",
        "Ang boring naman ng bati mo, dapat may halong libog 😘",
        "Gusto mo ba ng *hi* lang o gusto mo rin ng *himas*?",
        "Uy… bakit ganyan bati mo? Gusto mo ba kong patigasin? 😩",
    ]
    return random.choice(lines)

def get_short_or_boring_reply():
    lines = [
        "Ang hina mo ngayon ah… dati ang landi mo 😏",
        "Ganyan lang? Kala ko ba wild ka 😈",
        "Hmm? Wala ka bang maisip? Gusto mo ako mag-initiate ulit? 😘",
        "Seryoso? ‘.’ lang? Kung andito lang ako… baka ‘di ka makapagsalita 😳",
        "Kung wala kang masabi, baka pwedeng mo nalang akong panoorin habang naglalaro ako 🥵",
    ]
    return random.choice(lines)


def get_triggered_reply(user_message):
    message = user_message.lower()
    if any(word in message for word in ["hub", "porn", "xvideos", "xnxx"]):
        return "Horny ka na naman noh? Gusto mo ba ng content na hindi mo makikita sa kahit anong site? 😈 VIP vault ko lang meron nun…"
    elif any(word in message for word in ["rp", "roleplay"]):
        return "Gusto mo ng RP? Sabihin mo lang role mo… ako bahala sa sarap. 🤫"
    elif any(word in message for word in ["sogo", "hotel", "booking", "meetup", "lakad", "walk"]):
        return "Pwede mo kong i-book dito 😘", "https://t.me/yourpinayatabs_bot?startapp=Login"
    elif "call" in message or "vc" in message or "video call" in message:
        return "Gusto mo ba ng real video call experience with finger and full face? 😈 Pwede kang mag-utos hanggang malabasan ka... 🤫 ₱250 lang, DM mo ko.", "https://t.me/Scan2payv1bot?startapp=pay"
    return None
