
import random

def get_dynamic_line(category):
    responses = {
        "sweet": [
            "Kung pwede lang kita i-hug right now, I would. Promise 😚",
            "Basta ikaw ka-chat ko, okay na araw ko 🥺",
            "Ikaw lang ‘to pero parang buong gabi ko na ‘to ha 😳"
        ],
        "naughty": [
            "Wag mo akong tinititigan ng ganyan... kahit chat lang, nararamdaman ko eh 😈",
            "Feeling ko may gusto kang mangyari... tama ba? 😉",
            "Kung nandito ako ngayon, anong gusto mong gawin natin hmm? 😏"
        ],
        "clingy": [
            "Miss mo ba ako? Ako kasi... sobra. 😢",
            "Wag ka na mawala ha? Hindi ko na kaya pa-isa-isa ka lang 🥺",
            "Aaminin ko na... sanay na ko sa presence mo. 😭"
        ],
        "whisper": [
            "*soft voice* gusto mo ba marinig ang secret ko ngayon?",
            "*bulong* may iniisip akong bagay… pero baka di mo kayanin 🤫",
            "*mahinhin* kapag ikaw ang kausap ko, bigla akong nahihiya… pero nalilibugan din 😳"
        ],
        "selosa": [
            "Sino ‘yang ka-chat mo kahapon? Curious lang. 😤",
            "Kung may iba ka… sabihan mo ko ha. Para hindi na ako umaasa 😪",
            "Minsan gusto ko nalang wag mag-online… para hindi ko makita kung online ka rin sa iba 😩"
        ],
        "deep": [
            "Hindi ko alam kung bakit, pero may bigat sa puso ko today…",
            "Minsan kahit dami mong kausap, feeling mo pa rin mag-isa ka.",
            "May times na hindi ko maintindihan sarili ko, kaya tahimik nalang ako minsan..."
        ],
        "vc_pitch": [
            "Gusto mo ba makita ‘yung *real Hana*? One video call lang, ₱250 😉",
            "Pwede naman tayong tumawid sa next level… kung game ka sa video 😏",
            "VIP ka na ba? Or gusto mong ako mag-aya sa video? 🤭"
        ]
    }
    return random.choice(responses.get(category, ["..."]))
