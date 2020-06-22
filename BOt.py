import config
import telebot
from neuralStyleTransfer import create_and_start

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)

    start_NST(message)
    photo(message)
def default_test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)
def start_NST(message):
    if message.text =='NST':
        create_and_start(config.setting)
def photo(message):
    if message.text =='NST':


        bot.send_photo(message.chat.id, open('замок.png', 'rb'));

if __name__ == '__main__':
     bot.infinity_polling()