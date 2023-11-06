import telebot
from token import money_name, TOKEN
from extensions import ConvertionException, CryptoConvector, Price

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите информацию в формате: \n<название исходной валюты> \ <название валюты, в которую требуется перевести> \ <сумма>\n Увидеть список доступных валют:/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in money_name.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def check(message: telebot.types.Message):
        try:
            value = message.text.split(' ')

            if len(value) != 3:
                raise ConvertionException('Вы ввели неверное число параметров')

            quote, base, amount = value
            total_base = CryptoConvector.convert(quote, base, amount)
        except ConvertionException as e:
            bot.reply_to(message, f'Ошибка ввода данных\n{e}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        else:
            text = Price.get_price(quote, base, amount)
            bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)