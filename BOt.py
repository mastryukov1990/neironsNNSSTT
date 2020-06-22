import config
import telebot
import os
from neuralStyleTransfer import create_and_start
from config import PathC, PathS

if not os.path.exists('content_photos'):
    os.makedirs('content_photos')
if not os.path.exists('style_photos'):
    os.makedirs('style_photos')


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types=["text",'photo'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    eho(message)

    start_NST(message)
    take_photo(message)
    photo(message)
    handle_docs_photo(message)



def handle_docs_photo(message):

    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src=PathS +'{}.jpg'.format(message.caption);

        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        bot.reply_to(message,"Фото добавлено: {name}".format(name= message.caption))

    except Exception as e:
        bot.reply_to(message,e )
def eho(message):
    if message.content_type == 'text':
        bot.send_message(message.chat.id, message.text)


def take_photo(message):
    if message.content_type=='photo':
        print(type(message.photo))


def start_NST(message):
    if message.text =='NST':
        create_and_start(config.setting)


def photo(message):
    if message.text =='NST':


        bot.send_photo(message.chat.id, open('замок.png', 'rb'));

if __name__ == '__main__':
     print('start working...')
     bot.infinity_polling()