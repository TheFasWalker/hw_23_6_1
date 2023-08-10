import telebot
from config import TOKEN, keys
from extensions import ConvertionException, ValuteConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'valutes'])
def help_function(message: telebot.types.Message):
    if message.text == '/start':
        text = 'Бот для конвертации валюты.\n Все вычисления основываются на информации с портала https://www.cryptocompare.com/'
    elif message.text == '/help':
        text = 'Как работать с ботом : \n Узнать список валют /valutes \n для произведения манипуляций с валятами введите клманду в формате \n <имя валюты><В какую валюту переводим><Количество переводимой валюты> '
    elif message.text == '/valutes':
        text = 'Доступные валюты:'
        for key in keys.keys():
            text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['voice'])
def vioce_alarm(message: telebot.types.Message):
    bot.reply_to(message,
                 'Простите, но у меня проблемы с динамиком на телефоне. \n Я немогу прослушать ваше сообщение.')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConvertionException('Слишком много входящих данных.')
        if len(values) < 3:
            raise ConvertionException('Слишком мало входящих данных.')
        valute1_input, valute2_input, count = values
        valute1 = valute1_input.lower()
        valute2 = valute2_input.lower()
        total = ValuteConverter.convert(valute1, valute2, count)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Неудалось обработать запрос\n {e}')
    else:
        text = f'{count} {valute1} = {total} {valute2}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
