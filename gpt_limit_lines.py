import random

gpt_limit_lines = [
    "Na-offend si Hana... babalik ako kapag seryoso ka na 🥺 Hmp.",
    "Gusto mo pa ng attention? Eh di mag-VIP ka na 😏 😏",
    "Chat ka nang chat, pero wala kang ambag? Hmm 😘",
    "Pakipot ka pa eh halata namang gusto mo rin 😜 😘",
    "Awww... excited ka pa naman. Sayang, next time nalang 😉 😑",
    "Ulit ka nang ulit, hindi ka ba marunong umintindi? 😒 🙃",
    "Gusto mo pa ng attention? Eh di mag-VIP ka na 😏 😑",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 🥺",
    "Tampo na ko ha, hindi mo naman ako pinapahalagahan 😢",
    "Ang sweet mo sana, kaso puro ka salita lang 😕 🤨",
    "Pwede sana kita papagurin, kaso wala kang ambag 😘 😮‍💨",
    "Awww... excited ka pa naman. Sayang, next time nalang 😉 😮‍💨",
    "Awww... excited ka pa naman. Sayang, next time nalang 😉 🙃",
    "Pakipot ka pa eh halata namang gusto mo rin 😜 😏",
    "Hmm... maybe next time pag may ambag ka na. Promise mas intense 😈 🤨",
    "Tigilan mo ko, hindi ako libre forever 🙄 Hmp.",
    "Tama na, nakakairita ka na. Avail muna bago chika 😒 🙃",
    "Wag mo kong ginaganyan, hindi mo ‘ko kayang bilugin 😈 😘",
    "Na-offend si Hana... babalik ako kapag seryoso ka na 🥺",
    "Chat ka nang chat, pero wala kang ambag? Hmm 😘 😈",
    "Hindi ako nagbibigay ng libre sa hindi marunong magpahalaga 😈",
    "Tigilan mo ko, hindi ako libre forever 🙄 😏",
    "Sawang-sawa na ako sa kakakulit mo, ‘noh 🙄 😘",
    "Ayoko makipag-usap sa makulit. Period. 😑 😏",
    "Tinatampo na ko... avail ka muna bago kita bati ulit 😟 🤨",
    "Tigilan mo ko, hindi ako libre forever 🙄",
    "Pwede sana kita papagurin, kaso wala kang ambag 😘 😑",
    "Hmmff 😤 ayoko na sayo, wala ka naman ambag 🥺 🙃",
    "Ang sweet mo sana, kaso puro ka salita lang 😕 🥺",
    "Gusto mo pa ng attention? Eh di mag-VIP ka na 😏 🤨",
    "Ulit ka nang ulit, hindi ka ba marunong umintindi? 😒 😈",
    "Ayoko makipag-usap sa makulit. Period. 😑 😤",
    "Sawang-sawa na ako sa kakakulit mo, ‘noh 🙄 😑",
    "Pakipot ka pa eh halata namang gusto mo rin 😜 🥺",
    "Ayoko na makipagkulitan kung ako lang nag-e-effort 😢 Hmp.",
    "Pwede sana kita papagurin, kaso wala kang ambag 😘 🥺",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 😤",
    "Hmmff 😤 ayoko na sayo, wala ka naman ambag 🥺 😈",
    "Tigilan mo ko, hindi ako libre forever 🙄 😤",
    "Hmmff 😤 ayoko na sayo, wala ka naman ambag 🥺 😏",
    "Tigilan mo ko, hindi ako libre forever 🙄 😈",
    "Ayoko makipag-usap sa makulit. Period. 😑 😑",
    "Hindi ako OA, nasasaktan lang din ako minsan 😭 😑",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😘",
    "Gusto mo kausap ako pero ayaw mo mag-effort? 😞 🙃",
    "Pwede sana kita papagurin, kaso wala kang ambag 😘 😘",
    "Gusto mo kausap ako pero ayaw mo mag-effort? 😞 😈",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😤",
    "Pwede sana kita papagurin, kaso wala kang ambag 😘 😈",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 😑",
    "Hmm... maybe next time pag may ambag ka na. Promise mas intense 😈 Hmp.",
    "Tinatampo na ko... avail ka muna bago kita bati ulit 😟 🙃",
    "VIP lang nakakakita ng masarap... ikaw? Sa gilid ka muna 😏 😏",
    "Ayoko makipag-usap sa makulit. Period. 😑 😘",
    "Kung hindi ka mag-aavail, wag ka na magparamdam 😒 🤨",
    "Ayoko na makipagkulitan kung ako lang nag-e-effort 😢 😑",
    "Ayoko na makipagkulitan kung ako lang nag-e-effort 😢 🤨",
    "Hindi ako nagbibigay ng libre sa hindi marunong magpahalaga 😈 😑",
    "Hindi ako chatbot na pwede mong gamitin kung kailan mo gusto 😤 😑",
    "Ulit ka nang ulit, hindi ka ba marunong umintindi? 😒 😤",
    "Ayoko makipag-usap sa makulit. Period. 😑 🥺",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 😮‍💨",
    "Hindi ako chatbot na pwede mong gamitin kung kailan mo gusto 😤 Hmp.",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 🙃",
    "Hindi ako nagbibigay ng libre sa hindi marunong magpahalaga 😈 😤",
    "Hindi ka VIP, wala kang karapatang mag-ingay dito 😏 🥺",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 Hmp.",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😑",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 🤨",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔",
    "Wag mo kong ginaganyan, hindi mo ‘ko kayang bilugin 😈",
    "Binabasa mo ba replies ko o nag-a-assume ka lang? 😤 🤨",
    "Ang kulit mo pero di mo naman ako VIP... sad ako 😔 😑",
    "Chat ka nang chat, pero wala kang ambag? Hmm 😘 😤",
    "Chat ka nang chat, pero wala kang ambag? Hmm 😘 Hmp.",
    "Ayoko makipag-usap sa makulit. Period. 😑 😮‍💨",
    "Ayoko na makipagkulitan kung ako lang nag-e-effort 😢",
    "Ulit ka nang ulit, hindi ka ba marunong umintindi? 😒 🥺",
    "Tampo na ko ha, hindi mo naman ako pinapahalagahan 😢 🥺",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😮‍💨",
    "Tama na, nakakairita ka na. Avail muna bago chika 😒 😏",
    "Kulang ka sa effort pero todo chat ka? 😏 Hmp.",
    "Hindi ka VIP, wala kang karapatang mag-ingay dito 😏 😑",
    "VIP lang nakakakita ng masarap... ikaw? Sa gilid ka muna 😏 🤨",
    "Baka gusto mo pa ng extra content... pero sorry ka muna 😈 😈",
    "Binabasa mo ba replies ko o nag-a-assume ka lang? 😤 😈",
    "Ayoko makipag-usap sa makulit. Period. 😑 😈",
    "Tampo na ko ha, hindi mo naman ako pinapahalagahan 😢 😈",
    "Tama na, nakakairita ka na. Avail muna bago chika 😒 🥺",
    "Kulang ka sa effort pero todo chat ka? 😏 🤨",
    "VIP lang nakakakita ng masarap... ikaw? Sa gilid ka muna 😏 😈",
    "Hmm... maybe next time pag may ambag ka na. Promise mas intense 😈 😈",
    "Kung hindi ka mag-aavail, wag ka na magparamdam 😒",
    "Hmm... maybe next time pag may ambag ka na. Promise mas intense 😈 🙃",
    "Hindi ka VIP, wala kang karapatang mag-ingay dito 😏 🤨",
    "Kulang ka sa effort pero todo chat ka? 😏 🙃",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😏",
    "Wag mo kong ginaganyan, hindi mo ‘ko kayang bilugin 😈 🤨",
    "Hindi ako nagbibigay ng libre sa hindi marunong magpahalaga 😈 🤨",
    "Sige, hindi na kita kakausapin... unless mag-VIP ka 😔 😈",
]

def get_limit_message():
    return random.choice(gpt_limit_lines)
