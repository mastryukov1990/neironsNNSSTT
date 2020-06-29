import telebot
from telebot import types
from config import data_for_bot
inline_btn_1 = telebot.types.InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 =telebot.types.InlineKeyboardMarkup().add(inline_btn_1)
bot = telebot.TeleBot(data_for_bot['TOKEN'])
#bot.py
@bot.message_handler(commands=["start"])
def inline(message):
  key = types.InlineKeyboardMarkup()
  but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
  but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
  but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
  key.add(but_1, but_2, but_3)
  bot.send_message(message.chat.id, "ВЫБЕРИТЕ КНОПКУ", reply_markup=key)

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
  if c.data == 'NumberOne':
    bot.send_message(c.message.chat.id, 'Это кнопка 1')
  if c.data == 'NumberTwo':
    bot.send_message(c.message.chat.id, 'Это кнопка 2')
  if c.data == 'NumberTree':
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="NumberOne", callback_data="NumberOne")
    but_2 = types.InlineKeyboardButton(text="NumberTwo", callback_data="NumberTwo")
    but_3 = types.InlineKeyboardButton(text="NumberTree", callback_data="NumberTree")
    key.add(but_1, but_2, but_3)
    bot.send_message(c.message.chat.id, 'Это кнопка 3', reply_markup=key)
bot.polling()
