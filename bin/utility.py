import telegram

bot_token = "1750316913:AAGXSDe61TrwdT3Qd_r6xAS3MLe7tx-YlpM"

def send_message(user_id, message = "<b>CIAO</b>"):
    bot = telegram.bot.Bot(bot_token)
    bot.send_message(chat_id=user_id, text=message, parse_mode=telegram.ParseMode.HTML)

def get_Account_id(bot):
    return bot['message']['chat']['id']