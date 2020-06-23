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
        self.num_style= 1
        self.num_cont = 1
        self.mode = 'by_parts'
        self.start_message = '/StartT'
        self.stylePicmode = 'StylePic'
        self.contPicmode = 'ContPic'
    def handle_docs_photo(self,message):

        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            if self.pic_mode=='style':
                Path=self.PathS
                src = Path + '{}.jpg'.format(self.num_style);

            if self.pic_mode=='cont':
                Path=self.PathC
                src = Path + '{}.jpg'.format(self.num_cont);

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            if self.pic_mode=='style':
                self.bot.reply_to(message, "Фото стиля добавлено: {name}".format(name=self.num_style))
                if not src in self.style_srcs:
                    self.style_srcs.append(src)
                    self.num_style += 1
            if self.pic_mode=='cont':
                self.bot.reply_to(message, "Фото контента добавлено: {name}".format(name=self.num_cont))

                if not src in self.content_srcs:
                    self.content_srcs.append(src)
                    self.num_cont += 1

        except Exception as e:
            print('no')


    def eho(self,message):
        if message.content_type == 'text':
            self.bot.send_message(message.chat.id, "ВСе ок, я работаю)({})".format(message.text))
    def change_mod(self,message):
        if message.text == 'All':
            self.mode = "All"
        if message.text == 'by_parts':
            self.mode = "by_parts"

    def change_pic_mode(self,message):
        if message.text == self.stylePicmode:
            self.pic_mode='style'
        if message.text == self.contPicmode:
            print('here')
            self.pic_mode='cont'


    def take_photo(self,message):
        if message.content_type == 'photo':
            print(type(message.photo))
            print(self.content_srcs)
            print(self.style_srcs)
            print(self.pic_mode)


    def start_NST(self,message):
        if message.text == self.start_message:
           setting['style_imgs']=[]


           for scr in self.style_srcs:
                setting['style_imgs'].append(image_loader(scr))
           for scr in self.content_srcs:
               setting['content_img']=image_loader(scr)
               setting['input'] = image_loader(scr)
               setting['contPicname'] = str(self.num_cont)
               setting['mode']= self.mode
               create_and_start(setting)

               self.bot.send_photo(message.chat.id, open(setting['contPicname']+'.png', 'rb'))


    def help(self, message):
        if message.text == '/help' or message.text == '/start' :
            self.bot.send_message(message.chat.id,
'''Привет, я люблю переносить стили, готов и тебе помочь в этом. Для этого: 
1) Пришли по одиночке фотографии стиля в формате jpg(можешь пприслать сколько пожелаешь но поодиночке)
2) Когда наберешь нужное количесвто напиши ContentPic и пришли фотографии тоже в jpg, которые ты бы хотел разукрасить.
 Тоже по одиночке
 4)Пропиши  /StartT ля начала выполнения''')
    def photo(self,message):
        if message.text ==  self.start_message:
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
    def start_again(self,message):
        if message.text=='end':
            self.style_srcs = []
            self.content_srcs = []
            self.pic_mode = 'style'
            self.num_style = 1
            self.num_cont = 1
            self.mode = 'by_parts'
            self.start_message = '/StartT'

    def repeat_all_messages(self,message):  # Название функции не играет никакой роли, в принципе
        self.help(message)
        self.eho(message)
        self.start_NST(message)
        self.show(message)
        self.take_photo(message)
        #self.photo(message)
        self.handle_docs_photo(message)
        #self.exchange_command(message)
        self.change_pic_mode( message)
        self.change_mod(message)
        self.start_again( message)

print('start')
mybot = BBB(data_for_bot)
@mybot.bot.message_handler(content_types=["text", 'photo','command'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    mybot.repeat_all_messages(message)


mybot.bot.polling()