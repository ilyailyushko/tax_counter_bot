import telebot

bot = telebot.TeleBot("1217064730:AAECUm0tyh9z9SEz3i1y3BNKN7aN2dd_TuM")
original_sum = ''
original_tax = ''
welcome_msg = "Если надо выстваить счет юр лицу 👉 /6" + '\n\n' + "А если физ лицу 👉 /4"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, welcome_msg)


@bot.message_handler(commands=['4', '6'])
def fix_tax(message):
    global original_tax
    if message.text=='/4':
        original_tax = 4
        bot.reply_to(message, "👌 Физ лицо ➡️ будем платить 4% ")
    if message.text=='/6':
        original_tax = 6
        bot.reply_to(message, "👌 Юр лицо ➡️ заплатим 6% налога ")
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
        ok = '✅'
        msg = 'Надо выставить счет на 👉' + str(total_sum) + '\n\n'
        msg = msg + 'Сумма налога 👉' + str("%.2f" % (total_sum - total_sum_after_tax)) + "₽" + '\n\n'
        msg = msg + 'После уплаты налогов останется 👉' + str(total_sum_after_tax) + "₽"

        bot.send_message(message.chat.id, ok)
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.reply_to(message, '🤷‍♂️🔡 Это не число или что то пошло не так...')
        bot.reply_to(message, 'Давай начнием сначала' + '\n\n' + welcome_msg)


bot.polling()
