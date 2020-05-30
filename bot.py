import telebot

bot = telebot.TeleBot("1217064730:AAECUm0tyh9z9SEz3i1y3BNKN7aN2dd_TuM")
original_sum = ''
original_tax = ''
user_result = None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "Если вы собираетесь выстваить счет юр лицу 👉 /6 если физ лицу 👉 /4")

@bot.message_handler(commands=['4','6'])
def fix_tax(message):
    global original_tax
    if message.text == '/4':
        original_tax = 4
        bot.reply_to(message, "Ок, физ лицо, будем платить 4% ")
    if message.text == '/6':
        original_tax = 6
        bot.reply_to(message, "Ок, юр лицо, заплатим 6% налога ")
    msg = bot.send_message(message.chat.id, "Какая сумма должна зайти чистыми?")
    bot.register_next_step_handler(msg, fix_sum)
def fix_sum (message):
    global original_sum
    try:
        original_sum = int(message.text)
        print(original_sum, original_tax)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')

bot.polling()
