import telebot

bot = telebot.TeleBot("1217064730:AAECUm0tyh9z9SEz3i1y3BNKN7aN2dd_TuM")
original_sum = ''
original_tax = ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
        "Если вы собираетесь выстваить счет юр лицу 👉 /6 если физ лицу 👉 /4")


@bot.message_handler(commands=['4', '6'])
def fix_tax(message):
    global original_tax
    if message.text=='/4':
        original_tax = 4
        bot.reply_to(message, "Ок, физ лицо, будем платить 4% ")
    if message.text=='/6':
        original_tax = 6
        bot.reply_to(message, "Ок, юр лицо, заплатим 6% налога ")
    msg = bot.send_message(message.chat.id, "Какая сумма должна зайти чистыми?")
    bot.register_next_step_handler(msg, fix_sum)


def fix_sum(message):
    global original_sum
    try:
        original_sum = int(message.text)
        tax_value = 100 - original_tax
        total_sum = round(original_sum * 100 / tax_value)
        total_sum_after_tax = (total_sum - (total_sum / 100 * original_tax))
        if total_sum_after_tax < original_sum:
            total_sum = total_sum + 1
            total_sum_after_tax = (total_sum - (total_sum / 100 * original_tax))
        msg = 'Надо выставить счет на 👉', str(total_sum), "₽"
        msg += 'Сумма налога 👉', str("%.2f" % (total_sum - total_sum_after_tax)), "₽"
        msg += 'После уплаты налогов останется 👉', str(total_sum_after_tax), "₽"
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')

bot.polling()
