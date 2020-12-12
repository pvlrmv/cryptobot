import telebot
from config import keys, TOKEN
from extensions import ConvertionExcetion, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'чтобы начаь работу введите команду боту в следующем формате: \n<имя валюты цену которой он вы хотите узнать> \
<имя валюты в которой вы хотите узнать цену первой валюты> \
<количество первой валюты>'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'достуные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExcetion('Слишком много параметров. ')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except ConvertionExcetion as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')


    except Exception as e:
        bot.reply_to(message, f'не удалось обрпботаь команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)




bot.polling()
