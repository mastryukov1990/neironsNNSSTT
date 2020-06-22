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
        self.PathC = data_bot['PathC']
        self.style_srcs=[]
        self.content_srcs = []
        self.pic_mode = 'style'

    def handle_docs_photo(self,message):

        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            if self.pic_mode=='style':
                Path=self.PathS
            if self.pic_mode=='cont':
                Path=self.PathC
            src = Path + '{}.jpg'.format(message.caption);

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            self.bot.reply_to(message, "Фото добавлено: {name}".format(name=message.caption))

            if self.pic_mode=='style':
                if not src in self.style_srcs:
                    self.style_srcs.append(src)
            if self.pic_mode=='cont':
                if not src in self.content_srcs:
                    self.content_srcs.append(src)

        except Exception as e:
            print('no')


    def eho(self,message):
        if message.content_type == 'text':
            self.bot.send_message(message.chat.id, message.text)


    def change_pic_mode(self,message):
        if message.text == 'StylePic':
            self.pic_mode='style'
        if message.text == 'ContentPic':
            print('here')
            self.pic_mode='cont'


    def take_photo(self,message):
        if message.content_type == 'photo':
            print(type(message.photo))
            print(r.content_srcs)
            print(r.style_srcs)
            print(r.pic_mode)


    def start_NST(self,message):
        if message.text == 'NST':
           setting['style_imgs']=[]


           for scr in self.style_srcs:
                   setting['style_imgs'].append(image_loader(scr))
           for scr in self.content_srcs:
               setting['content_img']=image_loader(scr)
               setting['input'] = image_loader(scr)
               create_and_start(setting)


    def photo(self,message):
        if message.text == 'NST':
            self.bot.send_photo(message.chat.id, open('замок.png', 'rb'));


    def show(self,message):
        if message.text == 'покажи':
            self.bot.send_photo(message.chat.id, open(self.style_srcs[0], 'rb'));


    def exchange_command(self,message):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(  telebot.types.InlineKeyboardButton('USD', callback_data='get-USD')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
            telebot.types.InlineKeyboardButton('RUR', callback_data='get-RUR')
        )

        self.bot.send_message(
            message.chat.id,
            'Click on the currency of choice:',
            reply_markup=keyboard
        )


    def repeat_all_messages(self,message):  # Название функции не играет никакой роли, в принципе
        self.eho(message)
        self.start_NST(message)
        self.show(message)
        self.take_photo(message)
        self.photo(message)
        self.handle_docs_photo(message)
        self.exchange_command(message)
        self.change_pic_mode( message)

print('start')
r = BBB(data_for_bot)
@r.bot.message_handler(content_types=["text", 'photo'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    r.repeat_all_messages(message)




r.bot.polling()
