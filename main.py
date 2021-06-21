import telebot
import conf
from telebot import types
from bs4 import BeautifulSoup
import requests
# from threading import Timer

bot = telebot.TeleBot(conf.TOKEN)

global zodiac

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard = types.InlineKeyboardMarkup()
    aries_button = types.InlineKeyboardButton(text='овен', callback_data='aries')
    taurus_button = types.InlineKeyboardButton(text='телец', callback_data='taurus')
    gemini_button = types.InlineKeyboardButton(text='близнецы', callback_data='gemini')
    cancer_button = types.InlineKeyboardButton(text='рак', callback_data='cancer')
    leo_button = types.InlineKeyboardButton(text='лев', callback_data='leo')
    virgo_button = types.InlineKeyboardButton(text='дева', callback_data='virgo')
    libra_button = types.InlineKeyboardButton(text='весы', callback_data='libra')
    scorpio_button = types.InlineKeyboardButton(text='скорпион', callback_data='scorpio')
    sagittarius_button = types.InlineKeyboardButton(text='стрелец', callback_data='sagittarius')
    capricorn_button = types.InlineKeyboardButton(text='козерог', callback_data='capricorn')
    aquarius_button = types.InlineKeyboardButton(text='водолей', callback_data='aquarius')
    pisces_button = types.InlineKeyboardButton(text='рыбы', callback_data='pisces')
    keyboard.add(aries_button, taurus_button, gemini_button,
                 cancer_button, leo_button, virgo_button,
                 libra_button, scorpio_button, sagittarius_button,
                 capricorn_button, aquarius_button, pisces_button)
    bot.send_message(message.chat.id,
                     "Хотите узнать свой гороскоп на сегодня? Выберите свой знак зодиака", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global zodiac

    def get_horomail(zodiac):
        url_template = f'https://horo.mail.ru/prediction/{zodiac}/today/'
        url = requests.get(url_template).text
        soup = BeautifulSoup(url, 'html.parser')
        tags = soup.find('div', class_='article__item article__item_alignment_left article__item_html')
        for p in tags.find_all('p'):
            out = ''.join(p.text)
            bot.send_message(call.message.chat.id, out)

    def get_thousands_of_horoscopes(zodiac):
        url_template = f'https://1001goroskop.ru/?znak={zodiac}'
        url = requests.get(url_template).text
        soup = BeautifulSoup(url, 'html.parser')
        tags = soup.find('div', itemprop="description")
        horotext = tags.find('p')
        bot.send_message(call.message.chat.id, horotext)

    def get_horo_keyboard(call):
        keyboard = types.InlineKeyboardMarkup()
        horomail_button = types.InlineKeyboardButton(text='Гороскопы Майл.ру', callback_data='get_horomail')
        thousands_of_horoscopes_button = types.InlineKeyboardButton(text='1001 гороскоп',
                                                                    callback_data='get_thousands_of_horoscopes')
        keyboard.add(horomail_button, thousands_of_horoscopes_button)
        bot.send_message(call.message.chat.id, 'Ура! Пожалуйста, выберите гороскоп, который хотите получить',
                         reply_markup=keyboard)


    if call.message:
        if call.data == 'aries':
            zodiac = 'aries'
            get_horo_keyboard(call)
        if call.data == 'taurus':
            zodiac = 'taurus'
            get_horo_keyboard(call)
        if call.data == 'gemini':
            zodiac = 'gemini'
            get_horo_keyboard(call)
        if call.data == 'cancer':
            zodiac = 'cancer'
            get_horo_keyboard(call)
        if call.data == 'leo':
            zodiac = 'leo'
            get_horo_keyboard(call)
        if call.data == 'virgo':
            zodiac = 'virgo'
            get_horo_keyboard(call)
        if call.data == 'libra':
            zodiac = 'libra'
            get_horo_keyboard(call)
        if call.data == 'scorpio':
            zodiac = 'scorpio'
            get_horo_keyboard(call)
        if call.data == 'sagittarius':
            zodiac = 'sagittarius'
            get_horo_keyboard(call)
        if call.data == 'capricorn':
            zodiac = 'capricorn'
            get_horo_keyboard(call)
        if call.data == 'aquarius':
            zodiac = 'aquarius'
            get_horo_keyboard(call)
        if call.data == 'pisces':
            zodiac = 'pisces'
            get_horo_keyboard(call)
        if call.data == 'get_horomail':
            get_horomail(zodiac)
        if call.data == 'get_thousands_of_horoscopes':
            get_thousands_of_horoscopes(zodiac)

if __name__ == '__main__':
    bot.polling(none_stop=True)

