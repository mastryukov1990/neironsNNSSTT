import telebot
from config import data_for_bot,setting, image_loader, imshow
from neuralStyleTransfer import create_and_start
import os
import matplotlib.pyplot as plt
from NST import imshow1
import os
if not os.path.exists('content'):
    os.makedirs('content')
if not os.path.exists('content/style_photos'):
    os.makedirs('content/style_photos')
if not os.path.exists('content/content_photos'):
    os.makedirs('content/content_photos')
if not os.path.exists('content/final_photos'):
    os.makedirs('content/final_photos')
class BBB:
    def __init__(self,data_bot):
        self.bot = telebot.TeleBot(data_bot['TOKEN'])
        self.PathS=data_bot['PathS']
        self.PathC = data_bot['PathC']

        self.style_srcs=[]
        self.content_srcs = []

        self.pic_mode = 'style'
        self.stylePicmode = '/StylePic'
        self.contPicmode = '/ContPic'

        self.num_style= 1
        self.num_cont = 1

        self.mode = 'All'
        self.modeAll='/All'
        self.modeByParst= '/by_parts'

        self.start_message = '/run'

        self.standatrsize= 100
        self.size = [300,300]
        self.K=0.8

        self.epoches = 100
    def handle_docs_photo(self,message):

        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            chatid=str(message.chat.id)
            if not os.path.exists('content/content_photos/'+chatid):
                os.makedirs('content/content_photos/'+chatid)
            if not os.path.exists('content/style_photos/'+chatid):
                os.makedirs('content/style_photos/'+chatid)
            if self.pic_mode=='style':
                Path='content/style_photos/'+chatid+'/style_'
                print('here')
                src = Path + '{}.jpg'.format(str(self.num_style));

            if self.pic_mode=='cont':
                Path=self.PathC+chatid
                Path = 'content/content_photos/' + chatid + '/cont_'
                src = Path + '{}.jpg'.format(str(self.num_cont));

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                print('here')

            if self.pic_mode=='style':
                self.bot.reply_to(message,
                                  '''Фото стиля добавлено: {name} \nМожешь добавить еще, \nили начать добавлять контент-картинки(эти картинки я и буду менять) {mode}'''.format(name=self.num_style,mode=self.contPicmode))
                if not src in self.style_srcs:
                    self.style_srcs.append(src)
                    self.num_style += 1
            if self.pic_mode=='cont':
                self.bot.reply_to(message, '''Фото контента добавлено: {name}\nМожешь добавить еще, \nдополнить стиль-картинки {mode},\n и даже запустить волшебную трансформацию {start}
                                   '''.format(name=self.num_cont,
                                              mode= self.stylePicmode,
                                              start=self.start_message))

                if not src in self.content_srcs:
                    self.content_srcs.append(src)
                    self.num_cont += 1

        except Exception as e:
            print('not_photo')

    def checkworck(self,message):
        self.bot.send_message(message.chat.id, "ВСе ок, я работаю)".format(message.text))

    def eho(self,message):
        if message.text == 'ok?':
            self.checkworck(message)


    def change_mod(self,message):
        print('here')
        if message.text == '/All':
            self.mode = "All"
            self.bot.send_message(message.chat.id, "Работаю в режиме{}".format(self.mode))

        if message.text == '/by_parts':
            self.mode = "by_parts"
            self.bot.send_message(message.chat.id, "Работаю в режиме{}".format(self.mode))

    def change_pic_mode(self,message):
        if message.text == self.stylePicmode:
            self.pic_mode='style'
            self.bot.send_message(message.chat.id, "Принимаю стиль-картинки ")

        if message.text == self.contPicmode:
            print('here')
            self.pic_mode='cont'
            self.bot.send_message(message.chat.id, "Принимаю контент-картинки")


    def prozar(self,message):
        if message.text == '/super_min':
            self.epoches=50
            self.bot.send_message(message.chat.id, self.epoches)
        if message.text == '/min':
            self.epoches=90
            self.bot.send_message(message.chat.id, self.epoches)
        if message.text == '/med':
            self.epoches=180
            self.bot.send_message(message.chat.id, self.epoches)
        if message.text == '/max':
            self.epoches=270
            self.bot.send_message(message.chat.id, self.epoches)
        if message.text == '/super_max':
            self.epoches=360
            self.bot.send_message(message.chat.id, self.epoches)


    def chooosesize(self,message):
        if message.text == '/super_minS':
            self.size=[self.standatrsize,self.standatrsize*self.K]
            self.bot.send_message(message.chat.id,'Ну и качетсво ты выбрал{}'.format(self.size))
        if message.text == '/minS':
            self.size=[self.standatrsize*2,2*self.standatrsize*self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.size))
        if message.text == '/medS':
            self.size=[3*self.standatrsize,3*self.standatrsize*self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.size))
        if message.text == '/maxS':
            self.size=[4*self.standatrsize,4*self.standatrsize*self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.size))
        if message.text == '/super_maxS':
            self.size=[5*self.standatrsize,5*self.standatrsize*self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.size))

    def take_photo(self,message):
        if message.content_type == 'photo':
            print(type(message.photo))
            print(self.content_srcs)
            print(self.style_srcs)
            print(self.pic_mode)


    def start_NST(self,message):
        print('here')
        if message.text == self.start_message:
           setting['style_imgs']=[]
           chatid = str(message.chat.id)
           if not os.path.exists('content/final_photos/' + chatid):
               os.makedirs('content/final_photos/' + chatid)
           setting['size'] = self.size
           for scr in self.style_srcs:
                setting['style_imgs'].append(image_loader(scr,self.size))
           for scr,num in zip(self.content_srcs,range(len(self.content_srcs))):
               num+=1
               setting['content_img']=image_loader(scr,self.size)
               setting['input'] = image_loader(scr,self.size)
               setting['contPicname'] = 'content/final_photos/'+chatid+'/'+str(num)
               setting['mode']= self.mode

               setting['size'] = self.size
               setting['epoches'] = self.epoches
               create_and_start(setting)

               self.bot.send_photo(message.chat.id, open(setting['contPicname']+'.png', 'rb'))
           self.bot.send_message(message.chat.id,' еще хочу твоих фотографий, \n тыкни /end и повтори ')
    def foridiot(self, message):
        if message.text == '/start' or message.text == '/help':
            self.bot.send_message(message.chat.id,
''' Привет, я люблю переносить стили и готов тебе помочь:
1)  просто пришли мне стиль-картинку в jpg формате:) 
(с этой картинки я заберу стиль и перенесу на другую)
2)  Подробнее /more ''')

    def help(self, message):
        if message.text == '/more'  :
            self.bot.send_message(message.chat.id,
'''Подробнее: 

1) Пришли по одиночке фотографии стиля в формате jpg(можешь прислать сколько пожелаешь, но поодиночке)


2) Когда наберешь нужное количесвто напиши {ContentPic} и пришли фотографии тоже в jpg, которые ты бы хотел разукрасить.
Тоже по одиночке



 
3) Можете настроить на свой вкус(попробуй их всех): \n режим работы: {All} или {by_parts}
 
качество:
/super_minS, /minS, /medS, /maxS или /super_maxS !!!
 
степень изменения стиля: /min, /med, /max или /super_max

 
4)Пропиши  {StartT} ля начала выполнения



5) А если захочешь все сбросить и попробывать другие картинки просто напиши /end'''.format(ContentPic=self.contPicmode,
                                                   StartT=self.start_message,
                                                   All = self.modeAll,
                                                   by_parts=self.modeByParst))


    def photo(self,message):
        if message.text ==  self.start_message:
            self.bot.send_photo(message.chat.id, open('замок.png', 'rb'));


    def show(self,message):
        if message.text == 'покажи':
            self.bot.send_photo(message.chat.id, open(self.style_srcs[0], 'rb'));


    def exchange_command(self,message):

        button_hi = telebot.types.KeyboardButton('Привет! 👋')

        greet_kb = telebot.types.ReplyKeyboardMarkup()
        greet_kb.add(button_hi)
        inline_btn_1 = telebot.types.InlineKeyboardButton('Первая кнопка!', callback_data='button1')
        inline_kb1 = telebot.types.InlineKeyboardMarkup().add(inline_btn_1)

        self.bot.send_message(
            message.chat.id,
            'i do not know for what',
            reply_markup=inline_kb1
        )
    def start_again(self,message):
        if message.text=='/end':
            self.style_srcs = []
            self.content_srcs = []
            self.pic_mode = 'style'
            self.num_style = 1
            self.num_cont = 1
            self.mode = 'by_parts'

            self.bot.send_message(message.chat.id, 'Все обновилость!!! Начни по-новой /start')

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
        self.prozar(message)
        self.chooosesize( message)
        self.foridiot(message)
        #self.exchange_command( message)

print('start')
