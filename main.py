import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

from bin.menu import main_choise, dispo_choise, region_choise, province_choise

from bin import users_disponibility as ud, users as u

from bin.utility import send_message

from bin.file_creator import create_export_users_excel
bot_token = "1750316913:AAGXSDe61TrwdT3Qd_r6xAS3MLe7tx-YlpM"
genbot = telegram.bot.Bot(bot_token)


def gestore_callback(update: telegram.Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = update.callback_query.message.chat.id

    p = query.data.split("_")

    if p[0] == "master":
        if p[1] == "view":
            tmp = None
            if p[2] == "active":
                tmp = ud.get_users_active()
                send_message(user_id, message="<b>UTENTI ATTIVI ("+str(ud.count_active_users())+")</b>")
                print(tmp)
            elif p[2] == "inactive":
                tmp = ud.get_users_inactive()
                send_message(user_id, message="<b>UTENTI INATTIVI ("+str(ud.count_not_active_user())+")</b>")
            if tmp != None:
                for x in tmp:
                    stamp_user_info(user_id, x[0])
                query.edit_message_text("🚀🚀Richiesta inoltrata..🚀🚀")
        elif p[1] == "download":
            if p[2] == "excel":
                create_export_users_excel(user_id)
                query.edit_message_text("🚀🚀Richiesta inoltrata..🚀🚀")


    print(context)

    q = query.data.split('_')

    query.answer()


def aggiorna_posizione(bot, data):
    pass


def aggiorna_disponibilità(bot, data):
    dispo_choise(bot, data)


def registrer_user(bot, data):
    account_id = bot['message']['chat']['id']
    r = u.check_user_state(bot)

    r_text = "Scrivi nome e cognome:"
    u.singup(bot, data)
    genbot.send_message(chat_id=account_id, text=r_text, parse_mode=telegram.ParseMode.HTML)

    u.set_user_state(bot, data, 1)

    main_choise(bot, data)


def return_to_menu(bot, data):
    main_choise(bot, data)


def aggiorna_dis_s(bot, data):
    account_id = bot["message"]["chat"]["id"]

    print(u.get_avaib(account_id))
    if u.get_avaib(account_id) == 0:
        u.set_avaib(account_id, 1)
        u.set_last_disponibility(account_id)

    else:
        genbot.send_message(account_id, "Sei già disponibile..",
                            parse_mode=telegram.ParseMode.HTML)


def aggiorna_dis_n(bot, data):
    account_id = bot["message"]["chat"]["id"]

    if u.get_avaib(account_id) == 1:
        u.set_avaib(account_id, 0)
        u.set_last_disponibility(account_id)

    else:
        genbot.send_message(account_id, "Già non sei disponibile..",
                            parse_mode=telegram.ParseMode.HTML)

    region_flag = u.check_region(account_id)
    province_flag = u.check_province(account_id)

    print([province_flag, region_flag])
    if not region_flag and not province_flag:
        send_message(account_id, "<b>Ricorda di inserire regione e provincia..</b>")
    elif not region_flag:
        send_message(account_id, "<b>Ricorda di inserire la regione</b>")
    elif not province_flag:
        send_message(account_id, "<b>Ricorda di inserire la provincia</b>")

def insert_name_surname(bot, data):
    account_id = bot['message']['chat']['id']

    if u.check_user_state(bot) == 1:
        s = bot["message"]["text"].split(' ')

        name = s[0]
        surname = s[1]
        u.set_name_surname(bot, data, name, surname)

        u.set_user_state(bot, data, 2)
    else:
        genbot.send_message(account_id, "INPUT ERRATO", parse_mode=telegram.ParseMode.HTML)


import datetime


def update_date(bot, data):
    account_id = bot["message"]["chat"]["id"]

    m = bot.message.text
    l = str(m).split(' ')

    start = l[0]
    end = l[len(l) - 1]
    try:
        start = datetime.datetime.strptime(start, "%d/%m/%Y").date()
        end = datetime.datetime.strptime(end, "%d/%m/%Y").date()
        if start > end:
            send_message(account_id, "Data di inizio sbagliata")
    except:
        send_message(account_id, "Date inserite non valide..")

    u.update_start_date(account_id, start)
    u.update_end_date(account_id, end)

def gestore_regioni_dipendenti(bot: telegram.update.Update, data: telegram.ext.callbackcontext.CallbackContext):
    account_id = bot["message"]["chat"]["id"]
    region = str(bot.message.text).split('⚫')[1][1:]
    print(data)

    province_choise(bot, data, region)
    u.set_region(account_id, region)
    u.reset_province(account_id)
    #genbot.delete_message(account_id, bot.message.message_id) per cancellare i messagggii


def stamp_user_info(user_id, id):
    name = u.get_name_by_id(id)
    surname = u.get_surname_by_id(id)
    region = u.get_region_by_id(id)
    province = u.get_province_by_id(id)
    dispo = u.get_dispo_by_id(id)
    last_dispo = u.get_last_disp(id)

    tmp_position = None

    if region == None and province == None:
        tmp_position = "Non inserita.."
    else:
        tmp_position = str(region) + ", " + str(province)
    output = "<i>NOME: </i><b>" + str(name) + "</b>\n"
    output += "<i>COGNOME: </i><b>" + str(surname) + "</b>\n"
    output += "<i>ULTIMA POSZIONE: </i><b>" + tmp_position + "</b>\n"
    if str(dispo) == "SI":
        output += "<i>DISPONIBILITA': </i><b>SI ✔</b>\n"

    elif str(dispo) == "NO":
        output += "<i>DISPONIBILITA': </i><b>NO ❌</b>\n"
    else:
        output += "<i>DISPONIBILITA': </i><b>None</b>\n"
    output += "<i>ULTIMA CONFERMA: </i><b>" + str(last_dispo) + "</b>\n"

    send_message(user_id, message=output)
    
def gestore_regioni_master(bot: telegram.update.Update, data: telegram.ext.callbackcontext.CallbackContext):
    account_id = bot["message"]["chat"]["id"]
    region = str(bot.message.text).split('⚫')[1][1:]
    print(data)

    print(bot)

    if u.check_master(account_id):
        tmp = u.get_users_by_region(region)
        print(tmp)
        for x in tmp:
            print(x[0])
            stamp_user_info(account_id, x[0])
            main_choise(bot, data)



def gestore_provice(bot, data):
    account_id = bot["message"]["chat"]["id"]
    print(bot)
    province = str(bot.message.text).split('🟢')[1][1:]
    print(province)
    if u.check_master(account_id):
        tmp = u.get_users_by_province(province)
        print(tmp)
        for x in tmp:
            print(x[0])
            stamp_user_info(account_id, x[0])
            ud.add_session(account_id)

    else:
        u.set_province(account_id,province)
    main_choise(bot, data)

def stampa_regioni_master(bot, data):
    region_choise(bot, data, 1)

def stampa_master_ricerca_regionale(bot, data):
    region_choise(bot, data, 2)


def stampa_province_master(bot, date):
    province_choise(bot,date,flag=True)

def get_stat_master(bot, data):
    account_id = bot["message"]["chat"]["id"]
    if u.check_master(account_id):

        send_message(account_id, message="<i>✅N. DIPENDENTI DISPONIBILI: </i><b>" + str(ud.count_active_users()) + "</b>\n" +
                                         "<i>❎N. NON DIPENDENTI DISPONIBILI: </i><b>" + str(ud.count_not_active_user()) + "</b>\n")
        keyboard1 = [
                        [InlineKeyboardButton("VISUALIZZA ATTIVI", callback_data="master_view_active"),InlineKeyboardButton("VISUALIZZA INATTIVI", callback_data="master_view_inactive")],
                        [InlineKeyboardButton("📝SCARICA DATI", callback_data="master_download_excel")]
                     ]
        reply_markup = InlineKeyboardMarkup(keyboard1)
        bot.message.reply_html(text="<b>OPTIONS</b>",reply_markup=reply_markup)

        #genbot.delete_message(account_id, bot.message.message_id, timeout=3)


def stampa_utenti_by_province(bot, data):
    account_id = bot["message"]["chat"]["id"]
    print("STAMPA UTENTI BY PROVINCIA")

    province = str(bot.message.text).split('⚪')[1][1:]
    if u.check_master(account_id):
        tmp = ud.get_users_by_province(province)
        print(tmp)
        for x in tmp:
            print(x[0])

            stamp_user_info(account_id, x[0])
            ud.add_session(account_id)
            main_choise(bot, data)


def stampa_utenti_by_regioni(bot, data):
    account_id = bot["message"]["chat"]["id"]
    print("STAMPA UTENTI BY REGIONE")

    region = str(bot.message.text).split('🟠')[1][1:]
    if u.check_master(account_id):
        tmp = ud.get_users_by_region(region)

        output = "<i>N.DIPENDENTI IN "+region+"</i>: <b>"+str(ud.count_users_by_region(region))+"</b>\n"
        output += "<i>✅DIPENDENTI ATTIVI: </i><b>"+str(ud.count_active_users_by_region(region))+"</b>\n"
        output += "<i>❌DIPENDENTI INATTIVI: </i><b>"+str(ud.count_not_active_users_by_region(region))+"</b>\n"
        send_message(account_id, output)
        print(tmp)
        for x in tmp:
            print(x[0])

            stamp_user_info(account_id, x[0])
            ud.add_session(account_id)
            main_choise(bot, data)
def main():
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', registrer_user))
    dp.add_handler(CallbackQueryHandler(gestore_callback))
    dp.add_handler(MessageHandler(Filters.text("POSIZIONE"), callback=region_choise))
    dp.add_handler(MessageHandler(Filters.text("TORNA A REGIONI"), callback=region_choise))
    dp.add_handler(MessageHandler(Filters.text("DISPONIBILITA'"), callback=aggiorna_disponibilità))
    dp.add_handler(MessageHandler(Filters.text("SONO DISPONIBILE"), callback=aggiorna_dis_s))
    dp.add_handler(MessageHandler(Filters.text("NON SONO DISPONIBILE"), callback=aggiorna_dis_n))

    #FUNZIONI MASTER
    #dp.add_handler(MessageHandler(Filters.text("CERCA PER REGIONE"), callback=stampa_regioni_master))
    dp.add_handler(MessageHandler(Filters.text("CERCA PER PROVINCIA"), callback=stampa_regioni_master))
    dp.add_handler(MessageHandler(Filters.text("CERCA PER REGIONE"), callback=stampa_master_ricerca_regionale))
    dp.add_handler(MessageHandler(Filters.text("STATISTICHE"), callback=get_stat_master))


    dp.add_handler(MessageHandler(Filters.text("MENU"), callback=main_choise))

    dp.add_handler(MessageHandler(Filters.regex(r'⚫{1} [a-zA-Z ]{5,25}'), callback=gestore_regioni_dipendenti))#pallino nero
    dp.add_handler(MessageHandler(Filters.regex(r'🟢{1} [a-zA-Z ]{5,30}'), callback=gestore_provice))#pallino verde
    dp.add_handler(MessageHandler(Filters.regex(r'🔵{1} [a-zA-Z ]{3,30}'), callback=stampa_province_master))#pallino blu
    dp.add_handler(MessageHandler(Filters.regex(r'⚪{1} [a-zA-Z ]{3,30}'), callback=stampa_utenti_by_province))#pallino bianco
    dp.add_handler(MessageHandler(Filters.regex(r'🟠{1} [a-zA-Z ]{3,30}'), callback=stampa_utenti_by_regioni))  # pallino arancione



    dp.add_handler(MessageHandler(Filters.regex(r'[A-Z]{1}[a-z]{1,32} [A-Z]{1}[a-z]{1,32}'), callback=insert_name_surname))

    """dp.add_handler(MessageHandler(Filters.regex(r'[0-9]{0,1}[0-9]\/[0-9]{0,1}[0-9]\/[0-9]{4} {1,32}[0-9]{0,1}[0-9]\/[0-9]{0,1}[0-9]\/[0-9]{4}'),
                                  callback=update_date))
"""
    """dp.add_handler(CommandHandler('start', main_choise))
    dp.add_handler(CommandHandler('add', add_orders))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text("ORDERS"), callback=print_last_orders))
    dp.add_handler(MessageHandler(Filters.text("MENU"), callback=menu_choise))
    dp.add_handler(MessageHandler(Filters.text("MAIN MENU"), callback=main_choise))
    dp.add_handler(MessageHandler(Filters.text("WEEDS"), callback=show_weeds))
    dp.add_handler(MessageHandler(Filters.text("HASH"), callback=show_hash))
    dp.add_handler(MessageHandler(Filters.text("CALI"), callback=show_cali))


    dp.add_handler(MessageHandler(Filters.text("CARTS"), callback=show_cart))
    dp.add_handler(MessageHandler(Filters.text("REFRESH CART"), callback=show_cart))

    dp.add_handler(MessageHandler(Filters.text("DELETE ORDER"), callback=delete_cart))
    dp.add_handler(MessageHandler(Filters.text("CONFIRM ORDER"), callback=confirm_cart_by_user_id))
    dp.add_handler(MessageHandler(Filters.regex(r'([ a-zA-Z0-9 ]{1,64},*,[ a-zA-Z0-9 ]{1,64}){6,}'), callback=set_personal_values))
    updater.dispatcher.add_handler(CallbackQueryHandler(gestore_callback))"""
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    while True:
        main()
        try:
            pass
        except:
            print("BOT OFFLINE")
