from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext, \
    ConversationHandler
from utility import send_message, get_Account_id
from users import check_master, get_users_by_region
def stat(bot, data):
    account_id = get_Account_id(bot)

    if check_master(account_id):
        send_message(account_id, message="<i>N. DISPONIBILI: </i>"
                                         "N. NON DISPONIBILI: </i>"
                                         "N. DISPONIBILI NELLE ULTIME 24h: </i>"
                                         "N. "
                                         "")

def search_by_region(bot, update):
    account_id = get_Account_id(bot)

    if check_master(account_id):
        pass
def search_by_province(bot, update):
    account_id = get_Account_id(bot)

    if check_master(account_id):
        pass
def deployeer_state(bot, data):
    account_id = get_Account_id(bot)

    if check_master(account_id):
        pass

def graph(bot, data):
    account_id = get_Account_id(bot)

    if check_master(account_id):
        pass