from telegram import KeyboardButton, ReplyKeyboardMarkup
from .users import check_master, get_provinces
from .utility import get_Account_id
import bin.users_disponibility as ud

def main_keyboard():
    keyboard = [[KeyboardButton('POSIZIONE', callback_data='position')],
                [KeyboardButton("DISPONIBILITA'", callback_data='dispo')],
                [KeyboardButton("PROFILO", callback_data='profilo')]
                ]
    return ReplyKeyboardMarkup(keyboard)

def master_keyboard():
    keyboard = [[KeyboardButton('STATISTICHE', callback_data='master_stat')],
                [KeyboardButton("CERCA PER REGIONE", callback_data='master_region_search')],
                [KeyboardButton("CERCA PER PROVINCIA", callback_data='master_province_search')]
                ]
    return ReplyKeyboardMarkup(keyboard)


def main_message():
    return 'Choose the option in main menu:'



def main_choise(bot, update):
    account_id = get_Account_id(bot)
    if check_master(account_id):
        reply_markup = master_keyboard()
        bot.message.reply_text(main_message(), reply_markup=reply_markup)
    else:
        reply_markup = main_keyboard()
        bot.message.reply_text(main_message(), reply_markup=reply_markup)

def dispo_keyboard():
    keyboard = [[KeyboardButton('SONO DISPONIBILE', callback_data='disponibilita_yes'), KeyboardButton("NON SONO DISPONIBILE", callback_data='disponibilita_no')],
                [KeyboardButton("MENU", callback_data='menu')]]
    return ReplyKeyboardMarkup(keyboard)


def dispo_message():
    return 'Choose the option in main menu:'

def dispo_choise(bot, update):
    reply_markup = dispo_keyboard()
    bot.message.reply_text(dispo_message(), reply_markup=reply_markup)
keyboard = [[KeyboardButton('MENU', callback_data='menu')],
                [KeyboardButton('⚫ ABRUZZO', callback_data='region_abruzzo')],
                [KeyboardButton('⚫ BASILICATA', callback_data='region_basilicata')],
                [KeyboardButton('⚫ CALABRIA', callback_data='region_calabria')],
                [KeyboardButton('⚫ CAMPANIA', callback_data='region_campania')],
                [KeyboardButton('⚫ EMILIA-ROMAGNA', callback_data='region_emiliaromagna')],
                [KeyboardButton('⚫ FRIULI VENEZIA GIULIA', callback_data='region_friuli')],
                [KeyboardButton('⚫ LAZIO', callback_data='region_lazio')],
                [KeyboardButton('⚫ LIGURIA', callback_data='region_liguria')],
                [KeyboardButton('⚫ LOMBARDIA', callback_data='region_lombardia')],
                [KeyboardButton('⚫ MARCHE', callback_data='region_marche')],
                [KeyboardButton('⚫ MOLISE', callback_data='region_molise')],
                [KeyboardButton('⚫ PIEMONTE', callback_data='region_piemonte')],
                [KeyboardButton('⚫ PUGLIA', callback_data='region_puglia')],
                [KeyboardButton('⚫ SARDEGNA', callback_data='region_sardegna')],
                [KeyboardButton('⚫ SICILIA', callback_data='region_sicilia')],
                [KeyboardButton('⚫ TOSCANA', callback_data='region_toscana')],
                [KeyboardButton('⚫ TRENTINO-ALTO ADIGE', callback_data='region_trentino')],
                [KeyboardButton('⚫ UMBRIA', callback_data='region_umbria')],
                [KeyboardButton("⚫ VALLE D'AOSTA", callback_data='region_aosta')],
                [KeyboardButton("⚫ VENETO", callback_data='region_veneto')]
                ]


def region_keyboard():

    return ReplyKeyboardMarkup(keyboard)


def region_message():
    return 'Scegli la regione in cui ti trovi:'

def region_choise(bot, update, flag = 0):

    if flag == 0:
        reply_markup = region_keyboard()
        bot.message.reply_text(region_message(), reply_markup=reply_markup)
    elif flag == 1:
        tmp = []

        for k in ud.get_regions():
            tmp.append([KeyboardButton("🔵 "+str(k), callback_data='region_'+str(k).lower())])
        tmp.insert(0,[KeyboardButton('MENU', callback_data='menu')])
        reply_markup = ReplyKeyboardMarkup(tmp)
        bot.message.reply_text(region_message(), reply_markup=reply_markup)
    elif flag == 2:
        tmp = []

        for k in ud.get_regions():
            tmp.append([KeyboardButton("🟠 " + str(k), callback_data='region_' + str(k).lower())])#pallino arancione
        tmp.insert(0, [KeyboardButton('MENU', callback_data='menu')])
        reply_markup = ReplyKeyboardMarkup(tmp)
        bot.message.reply_text(region_message(), reply_markup=reply_markup)

province_abruzzo = ["Chieti", "L'Aquila", "Pescara", "Teramo"]
province_basilicata = ["Matera", "Potenza"]
province_calabria = ["Catanzaro", "Cosenza", "Crotone", "REGGIO CALABRIA", "Vibo Valentina"]
province_campania = ["Avellino", "Benevento", "Caserta", "NAPOLI", "Salerno"]
province_emilia = ["BOLOGNA", "Ferrara", "Forlì-Cesena", "Modena", "Parma", "Piacenza", "Ravenna", "Reggio Emilia", "Rimini"]
province_friuli = ["Gorizia", "Pordenone", "Trieste", "Udine"]
province_lazio = ["Frosinone", "Latina", "ROMA", "Viterbo"]
province_liguria = ["GENOVA", "Imperia", "La Spezia", "Savoia"]
province_lombardia = ["Bergamo", "Brescia", "Como", "Cremona", "Lecco", "Lodi", "Mantova", "MILANO", "Monza", "Pavia", "Sondrio", "Varese"]
province_marche = ["Ancona", "Ascoli Piceno", "Fermo", "Macerata", "Pesaro e Urbino"]
province_molise = ["Campobasso", "Isernia"]
province_piemonte = ["Alessandria", "Asti", "Biella", "Cuneo", "Novara", "TORINO", "Verbano-Cusio-Ossola"]
province_puglia = ["BARI", "Barletta-Adria-Trani", "Brindisi", "Foggia", "Lecce", "Taranto"]
province_sardegna = ["CAGLIARI", "Nuoro", "Oristano", "Sassari", "Sud Sardegna"]
province_sicilia = ["Agrigento", "Caltanissetta", "CATANIA", "Enna", "MESSINA", "PALERMO", "Ragusa", "Siracusa", "Trapani"]
province_toscana = ["Arezzo", "FIRENZE", "Grosseto", "Livorno", "Lucca", "Massa-Carrara", "Pisa", "Pistoia", "Prato", "Siena"]
province_trentino = ["Bolzano", "Trento"]
province_umbria = ["Perugia", "Terni"]
province_aosta = ["Aosta"]
province_veneto = ["Belluno", "Padova", "Rovigo", "Treviso", "VENEZIA", "Verona", "Vicenza"]


def province_keyboard(province=None):

    if province != None:
        keyboard = []

        if province == "ABRUZZO":
            for x in province_abruzzo:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "BASILICATA":
            for x in province_basilicata:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "CALABRIA":
            for x in province_calabria:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "CAMPANIA":
            for x in province_campania:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "EMILIA-ROMAGNA":
            for x in province_emilia:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "FRIULI VENEZIA GIULIA":
            for x in province_friuli:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "LAZIO":
            for x in province_lazio:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "LIGURIA":
            for x in province_liguria:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "LOMBARDIA":
            for x in province_lombardia:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "MARCHE":
            for x in province_marche:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "MOLISE":
            for x in province_molise:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "PIEMONTE":
            for x in province_piemonte:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "PUGLIA":
            for x in province_puglia:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_"+tmp2)])
        elif province == "SARDEGNA":
            for x in province_sardegna:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "SICILIA":
            for x in province_sicilia:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "TOSCANA":
            for x in province_toscana:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "TRENTINO-ALTO ADIGE":
            for x in province_trentino:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "UMBRIA":
            for x in province_umbria:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "VALLE D'AOSTA":
            for x in province_aosta:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])
        elif province == "VENETO":
            for x in province_veneto:
                tmp = "🟢 "+str(x).upper()
                tmp2 = str(x).lower()
                keyboard.append([KeyboardButton(tmp, callback_data="province_" + tmp2)])

        keyboard.insert(0, [KeyboardButton("TORNA A REGIONI", callback_data='menu')])
        return ReplyKeyboardMarkup(keyboard)


def province_message():
    return 'Sceglia la provincia di afferenza:'

def province_choise(bot, update, province = None, flag = False):
    f = str(bot.message.text).split(' ')[0]
    if flag == True:

        f2 = str(bot.message.text).split('🔵')[1]

        print(f2[1:])
        tmp = []
        p = get_provinces(bot["message"]["chat"]["id"], f2[1:])

        print(p)
        for k in p:
            if k != None:
                tmp.append([KeyboardButton("⚪ "+str(k), callback_data='region_'+str(k).lower())])
        tmp.insert(0,[KeyboardButton('MENU', callback_data='menu')])
        reply_markup = ReplyKeyboardMarkup(tmp)
        bot.message.reply_text(dispo_message(), reply_markup=reply_markup)
    else:
        reply_markup = province_keyboard(province)
        bot.message.reply_text(dispo_message(), reply_markup=reply_markup)


