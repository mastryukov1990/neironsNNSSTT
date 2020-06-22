import telebot
from config import data_for_bot,setting, image_loader, imshow
from neuralStyleTransfer import create_and_start
import os
import matplotlib.pyplot as plt
from NST import imshow1
if not os.path.exists('content_photos'):
    os.makedirs('content_photos')
if not os.path.exists('style_photos'):
    os.makedirs('style_photos')

class BBB:
    def __init__(self,data_bot):
        self.bot = telebot.TeleBot(data_bot['TOKEN'])
        self.PathS=data_bot['PathS']
        self.srcs=[]


    def handle_docs_photo(self,message):

        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            src = self.PathS + '{}.jpg'.format(message.caption);

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            self.bot.reply_to(message, "Фото добавлено: {name}".format(name=message.caption))
            if not src in self.srcs:
                self.srcs.append(src)
        except Exception as e:
            print('no')


    def eho(self,message):
        if message.content_type == 'text':
            self.bot.send_message(message.chat.id, message.text)

    def take_photo(self,message):
        if message.content_type == 'photo':
            print(type(message.photo))
            print(r.srcs)

    def start_NST(self,message):
        if message.text == 'NST':
           setting['style_imgs']=[]
           for scr in self.srcs:
               setting['style_imgs'].append(image_loader(scr))
           create_and_start(setting)

    def photo(self,message):
        if message.text == 'NST':
            self.bot.send_photo(message.chat.id, open('замок.png', 'rb'));
    def show(self,message):
        if message.text == 'покажи':
            self.bot.send_photo(message.chat.id, open(self.srcs[0], 'rb'));


    def repeat_all_messages(self,message):  # Название функции не играет никакой роли, в принципе
        self.eho(message)
        self.start_NST(message)
        self.show(message)
        self.take_photo(message)
        self.photo(message)
        self.handle_docs_photo(message)


print('start')
r = BBB(data_for_bot)
@r.bot.message_handler(content_types=["text", 'photo'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    r.repeat_all_messages(message)
r.bot.polling()
