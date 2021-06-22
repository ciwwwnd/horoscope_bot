import telebot
import conf
from telebot import types
from bs4 import BeautifulSoup
import requests
import json

# json_string = json.dumps(arr)


bot = telebot.TeleBot(conf.TOKEN)

global zodiac
global data

with open('data.json', 'w', encoding='utf-8') as f:
    json.dumps({})


def save_id(zodiac_dict):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(zodiac_dict, f, ensure_ascii=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Это бот-агрегатор гороскопов. Чтобы узнать свой гороскоп на сегодня вызовите команду /horo")


# собираем клавиатуру из знаков зодиака
@bot.message_handler(commands=['horo'])
def send_welcome(message):
    def handle_text(message):
        def get_another_keyboard(message):
            keyboard = types.InlineKeyboardMarkup()
            horomail_button = types.InlineKeyboardButton(text='Гороскопы Майл.ру', callback_data='get_horomail')
            thousands_of_horoscopes_button = types.InlineKeyboardButton(text='1001 гороскоп',
                                                                        callback_data='get_thousands_of_horoscopes')
            get_horo_365_button = types.InlineKeyboardButton(text='Гороскопы 365', callback_data='get_horo_365')
            keyboard.add(horomail_button, thousands_of_horoscopes_button, get_horo_365_button)
            bot.send_message(message.chat.id, 'Ура! Пожалуйста, выберите гороскоп, который хотите получить',
                             reply_markup=keyboard)

        get_horo_button = types.ReplyKeyboardMarkup(True, True)
        get_horo_button.row('Гороскоп')
        msg = bot.reply_to(message.chat.id, 'Получить гороскоп на сегодня', reply_markup=get_horo_button)
        bot.register_next_step_handler(msg, get_another_keyboard)

    def zodiac_keybord(message):
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
                         "Хотите узнать свой гороскоп на сегодня? Выберите знак зодиака", reply_markup=keyboard)

    with open('data.json', 'r', encoding='utf-8') as f:
        jsontext = f.read()
        if jsontext:
            global data
            data = json.loads(jsontext)
            if str(message.chat.id) in data.keys():
                # callback_inline.get_horo_keyboard(message)
                handle_text(message)
                zodiac_ = data[str(message.chat.id)]
                global zodiac
                zodiac = zodiac_
            else:
                zodiac_keybord(message)
        else:
            zodiac_keybord(message)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == 'Гороскоп':
        keyboard = types.InlineKeyboardMarkup()
        horomail_button = types.InlineKeyboardButton(text='Гороскопы Майл.ру', callback_data='get_horomail')
        thousands_of_horoscopes_button = types.InlineKeyboardButton(text='1001 гороскоп',
                                                                    callback_data='get_thousands_of_horoscopes')
        get_horo_365_button = types.InlineKeyboardButton(text='Гороскопы 365', callback_data='get_horo_365')
        keyboard.add(horomail_button, thousands_of_horoscopes_button, get_horo_365_button)
        bot.send_message(message.chat.id, 'Ура! Пожалуйста, выберите гороскоп, который хотите получить',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global zodiac

    def get_horomail(zodiac):
        """

        получаем гороскоп с сайта гороскопы майл.ру

        """
        url_template = f'https://horo.mail.ru/prediction/{zodiac}/today/'
        url = requests.get(url_template).text
        soup = BeautifulSoup(url, 'html.parser')
        tags = soup.find('div', class_='article__item article__item_alignment_left article__item_html')
        for p in tags.find_all('p'):
            out = ''.join(p.text)
            bot.send_message(call.message.chat.id, out)

    def get_thousands_of_horoscopes(zodiac):
        """

        получаем гороскоп с сайта гороскопы 1001 гороскоп

        """
        url_template = f'https://1001goroskop.ru/?znak={zodiac}'
        url = requests.get(url_template).text
        soup = BeautifulSoup(url, 'html.parser')
        tags = soup.find('div', itemprop="description")
        horotext = tags.find('p')
        bot.send_message(call.message.chat.id, horotext)

    def get_horo_365(zodiac):
        """

        получаем гороскоп с сайта гороскоп365

        """
        url_template = f'https://goroskop365.ru/{zodiac}/'
        url = requests.get(url_template).text
        soup = BeautifulSoup(url, 'html.parser')
        tags = soup.find('div', class_="content_wrapper horoborder")
        horotext = tags.find('p')
        bot.send_message(call.message.chat.id, horotext.text)

    def get_horo_keyboard(call):
        """

        собираем клавиатуру с тремя гороскопами

        """
        keyboard = types.InlineKeyboardMarkup()
        horomail_button = types.InlineKeyboardButton(text='Гороскопы Майл.ру', callback_data='get_horomail')
        thousands_of_horoscopes_button = types.InlineKeyboardButton(text='1001 гороскоп',
                                                                    callback_data='get_thousands_of_horoscopes')
        get_horo_365_button = types.InlineKeyboardButton(text='Гороскопы 365', callback_data='get_horo_365')
        keyboard.add(horomail_button, thousands_of_horoscopes_button, get_horo_365_button)
        bot.send_message(call.message.chat.id, 'Ура! Пожалуйста, выберите гороскоп, который хотите получить',
                         reply_markup=keyboard)

    if call.message:
        if call.data == 'aries':
            zodiac = 'aries'
            get_horo_keyboard(call)
            aries_dict = {str(call.message.chat.id): zodiac}
            save_id(aries_dict)
        if call.data == 'taurus':
            zodiac = 'taurus'
            get_horo_keyboard(call)
            taurus_dict = {str(call.message.chat.id): zodiac}
            save_id(taurus_dict)
        if call.data == 'gemini':
            zodiac = 'gemini'
            get_horo_keyboard(call)
            gemini_dict = {str(call.message.chat.id): zodiac}
            save_id(gemini_dict)
        if call.data == 'cancer':
            zodiac = 'cancer'
            get_horo_keyboard(call)
            cancer_dict = {str(call.message.chat.id): zodiac}
            save_id(cancer_dict)
        if call.data == 'leo':
            zodiac = 'leo'
            get_horo_keyboard(call)
            leo_dict = {str(call.message.chat.id): zodiac}
            save_id(leo_dict)
        if call.data == 'virgo':
            zodiac = 'virgo'
            get_horo_keyboard(call)
            virgo_dict = {str(call.message.chat.id): zodiac}
            save_id(virgo_dict)
        if call.data == 'libra':
            zodiac = 'libra'
            get_horo_keyboard(call)
            libra_dict = {str(call.message.chat.id): zodiac}
            save_id(libra_dict)
        if call.data == 'scorpio':
            zodiac = 'scorpio'
            get_horo_keyboard(call)
            scorpio_dict = {str(call.message.chat.id): zodiac}
            save_id(scorpio_dict)
        if call.data == 'sagittarius':
            zodiac = 'sagittarius'
            get_horo_keyboard(call)
            sagittarius_dict = {str(call.message.chat.id): zodiac}
            save_id(sagittarius_dict)
        if call.data == 'capricorn':
            zodiac = 'capricorn'
            get_horo_keyboard(call)
            capricorn_dict = {str(call.message.chat.id): zodiac}
            save_id(capricorn_dict)
        if call.data == 'aquarius':
            zodiac = 'aquarius'
            get_horo_keyboard(call)
            aquarius_dict = {str(call.message.chat.id): zodiac}
            save_id(aquarius_dict)
        if call.data == 'pisces':
            zodiac = 'pisces'
            get_horo_keyboard(call)
            pisces_dict = {str(call.message.chat.id): zodiac}
            save_id(pisces_dict)
        if call.data == 'get_horomail':
            get_horomail(zodiac)
        if call.data == 'get_thousands_of_horoscopes':
            get_thousands_of_horoscopes(zodiac)
        if call.data == 'get_horo_365':
            get_horo_365(zodiac)


if __name__ == '__main__':
    print('launching...')
    bot.polling(none_stop=True)
