import telebot
from telebot import types
from config import data_for_bot, setting, image_loader, imshow
from neuralStyleTransfer import create_and_start
import copy
import shutil
from PIL import Image
import numpy as np
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
    def __init__(self, data_bot):



        self.bot = telebot.TeleBot(data_bot['TOKEN'])
        self.PathS = data_bot['PathS']
        self.PathC = data_bot['PathC']

        self.style_srcs = []
        self.content_srcs = []

        self.pic_mode = 'style'
        self.stylePicmode = 'Стиль-картинки'
        self.contPicmode = 'Контент-картинки'

        self.num_style = 1
        self.num_cont = 1

        self.mode = 'All'
        self.modeAll = 'Все вместе'
        self.modeByParst = 'По частям'
        self.start_message = 'Трансформация'

        self.standatrsize = 100
        self.size = [300, 240]
        self.K = 0.8

        self.menumode = 'Главное меню'
        self.epoches = 100

        self.example={
            'style_srcs' : [],
            'content_srcs' : [],
            'pic_mode' : 'style',
            'num_style' : 1,
            'num_cont' : 1,
            'mode' : 'All',
            'size' : [300, 300],
            'epoches':100,
            'K' : 0.8,
            'transfer': 0,
            'menumode':'Главное меню'
        }
        self.userdict = {}
    def handle_docs_photo(self, message):
        try:
            print(self.userdict)
            print(self.example)
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            chatid = str(message.chat.id)

            if not os.path.exists('content/content_photos/' + chatid):
                os.makedirs('content/content_photos/' + chatid)
            if not os.path.exists('content/style_photos/' + chatid):
                os.makedirs('content/style_photos/' + chatid)
            if self.userdict[chatid]['pic_mode'] == 'style':
                Path = 'content/style_photos/' + chatid + '/style_'

                src = Path + '{}.jpg'.format(self.userdict[chatid]['num_style']);

            if self.userdict[chatid]['pic_mode'] == 'cont':
                Path = 'content/content_photos/' + chatid + '/cont_'
                src = Path + '{}.jpg'.format(self.userdict[chatid]['num_cont']);

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)


            if self.userdict[chatid]['pic_mode'] == 'style':
                self.bot.reply_to(message,
                                  '''Фото стиля добавлено: {name} \nМожешь добавить еще, \nили начать добавлять контент-картинки(эти картинки я и буду менять) {mode}'''.format(
                                      name=self.userdict[chatid]['num_style'], mode=self.contPicmode))
                if not src in self.userdict[chatid]['style_srcs']:
                    self.userdict[chatid]['style_srcs'].append(src)
                    self.userdict[chatid]['num_style'] += 1
            if self.userdict[chatid]['pic_mode'] == 'cont':
                self.bot.reply_to(message, '''Фото контента добавлено: {name}\nМожешь добавить еще, \nдополнить стиль-картинки {mode},\n и даже запустить волшебную трансформацию {start}
                                   '''.format(name=self.userdict[chatid]['num_cont'],
                                              mode=self.stylePicmode,
                                              start=self.start_message))

                if not src in self.userdict[chatid]['content_srcs']:
                    self.userdict[chatid]['content_srcs'].append(src)
                    self.userdict[chatid]['num_cont'] += 1
        except Exception as e:
            print('not_photo')


    def checkworck(self, message):
        self.bot.send_message(message.chat.id, "ВСе ок, я работаю)".format(message.text))

    def eho(self, message):
        chatid = str(message.chat.id)
        if not chatid in self.userdict:
            self.userdict[chatid] = copy.deepcopy(self.example)
            print( self.userdict[chatid])

    def change_mod(self, message):
        chatid =  str(message.chat.id)
        if message.text == self.modeAll:
            self.userdict[chatid]['mode'] = "All"
            self.bot.send_message(message.chat.id, "Работаю в режиме{}".format('Преобразую целиком'))

        if message.text == self.modeByParst:
            self.userdict[chatid]['mode'] = "by_parts"
            self.bot.send_message(message.chat.id, "Работаю в режиме  {}".format('Преобразую по частям'))

    def change_pic_mode(self, message):
        chatid =  str(message.chat.id)
        if message.text == self.stylePicmode:
            self.userdict[chatid]['pic_mode'] = 'style'
            self.bot.send_message(message.chat.id, "Принимаю стиль-картинки ")

        if message.text == self.contPicmode:
            print('here')
            self.userdict[chatid]['pic_mode']  = 'cont'
            self.bot.send_message(message.chat.id, "Принимаю контент-картинки")

    def prozar(self, message):
        chatid =  str(message.chat.id)

        if message.text == '/super_min':
            self.userdict[chatid]['epoches'] = 50
            self.bot.send_message(message.chat.id, self.userdict[chatid]['epoches'])

        if message.text == '/min':
            self.userdict[chatid]['epoches'] = 90
            self.bot.send_message(message.chat.id, self.userdict[chatid]['epoches'])

        if message.text == '/med':
            self.userdict[chatid]['epoches'] = 180
            self.bot.send_message(message.chat.id, self.userdict[chatid]['epoches'])

        if message.text == '/max':
            self.userdict[chatid]['epoches'] = 270
            self.bot.send_message(message.chat.id, self.userdict[chatid]['epoches'])

        if message.text == '/super_max':
            self.userdict[chatid]['epoches'] = 360
            self.bot.send_message(message.chat.id, self.userdict[chatid]['epoches'])
        self.quality = []

    def prozarC(self,c):
            chatid = str(c.message.chat.id)
            pathid = c.message.chat.id
            if c.data == 'ss':
                self.userdict[chatid]['epoches'] = 50
                self.bot.send_message(pathid, self.userdict[chatid]['epoches'])

            if c.data == 's':
                self.userdict[chatid]['epoches'] = 90
                self.bot.send_message(pathid, self.userdict[chatid]['epoches'])

            if c.data == 'm':
                self.userdict[chatid]['epoches'] = 180
                self.bot.send_message(pathid, self.userdict[chatid]['epoches'])

            if c.data == 'M':
                self.userdict[chatid]['epoches'] = 270
                self.bot.send_message(pathid, self.userdict[chatid]['epoches'])

            if c.data == 'SM':
                self.userdict[chatid]['epoches'] = 360
                self.bot.send_message(pathid, self.userdict[chatid]['epoches'])
            self.quality = []


    def chooosesize(self, message):
        chatid =  str(message.chat.id)
        if message.text == '/super_minS':
            self.userdict[chatid]['size'] = [self.standatrsize, self.standatrsize * self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if message.text == '/minS':
            self.userdict[chatid]['size'] = [self.standatrsize * 2, 2 * self.standatrsize * self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if message.text == '/medS':
            self.userdict[chatid]['size'] = [3 * self.standatrsize, 3 * self.standatrsize * self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if message.text == '/maxS':
            self.userdict[chatid]['size'] = [4 * self.standatrsize, 4 * self.standatrsize * self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if message.text == '/super_maxS':
            self.userdict[chatid]['size'] = [5 * self.standatrsize, 5 * self.standatrsize * self.K]
            self.bot.send_message(message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))


    def chooosesizeC(self, c):
        chatid =  str(c.message.chat.id)
        if c.data == 'ssS':
            self.userdict[chatid]['size'] = [self.standatrsize, self.standatrsize * self.K]
            self.bot.send_message(c.message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if c.data == 'sS':
            self.userdict[chatid]['size'] = [self.standatrsize * 2, 2 * self.standatrsize * self.K]
            self.bot.send_message(c.message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if c.data == 'mS':
            self.userdict[chatid]['size'] = [3 * self.standatrsize, 3 * self.standatrsize * self.K]
            self.bot.send_message(c.message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if c.data == 'MS':
            self.userdict[chatid]['size'] = [4 * self.standatrsize, 4 * self.standatrsize * self.K]
            self.bot.send_message(c.message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

        if c.data == 'SMS':
            self.userdict[chatid]['size'] = [5 * self.standatrsize, 5 * self.standatrsize * self.K]
            self.bot.send_message(c.message.chat.id, 'Ну и качетсво ты выбрал{}'.format(self.userdict[chatid]['size']))

    def change_modC(self,c):
        chatid = str(c.message.chat.id)
        if c.data == self.modeAll:
            self.userdict[chatid]['mode'] = "All"
            self.bot.send_message(c.message.chat.id, "Работаю в режиме  {}".format('Преобразую целиком'))

        if c.data == self.modeByParst:
            self.userdict[chatid]['mode'] = "by_parts"
            self.bot.send_message(c.message.chat.id, "Работаю в режиме  {}".format('Преобразую по частям'))

    def take_photo(self, message):
        if message.content_type == 'photo':
            print(type(message.photo))
            print(self.content_srcs)
            print(self.style_srcs)
            print(self.pic_mode)

    def start_NST(self, message):
        print('hereNST')
        local_setting = setting
        if message.text == self.start_message:
            print('hereNST')
            local_setting['style_imgs'] = []
            chatid = str(message.chat.id)
            self.userdict[chatid]['transfer']=1
            if not os.path.exists('content/final_photos/' + chatid):
                os.makedirs('content/final_photos/' + chatid)



            for scr, num in zip(self.userdict[chatid]['content_srcs'], range(len(self.userdict[chatid]['content_srcs']))):

                    num += 1

                    s = Image.open(scr).size
                    self.userdict[chatid]['size']= [self.userdict[chatid]['size'][0],int(self.userdict[chatid]['size'][0]*s[0]/s[1])]

                    local_setting['content_img']= image_loader(scr, self.userdict[chatid]['size'])
                    local_setting['input']= image_loader(scr, self.userdict[chatid]['size'])
                    local_setting['contPicname'] = 'content/final_photos/' + chatid + '/' + str(num)
                    local_setting['mode'] = self.userdict[chatid]['mode']
                    for scr in self.userdict[chatid]['style_srcs']:
                        local_setting['style_imgs'].append(image_loader(scr, self.userdict[chatid]['size']))

                    local_setting['size'] = self.userdict[chatid]['size']
                    local_setting['epoches'] = self.userdict[chatid]['epoches']
                    create_and_start(local_setting)

                    self.bot.send_photo(message.chat.id, open(local_setting['contPicname'] + '.png', 'rb'))
                    local_setting['style_imgs']=[]
            self.bot.send_message(message.chat.id,
'''Ура,получилось!!! 
Молодец, держишь уровень, как всегда говно''')
            self.userdict[chatid]['transfer'] = 0
    def create_bottons(self,data):
        key = types.InlineKeyboardMarkup()
        for text,call in data:

            but_1 = types.InlineKeyboardButton(text=text, callback_data=call)
            key.add(but_1)
        return  key


    def foridiot(self, message):
        if message.text == '/start' or message.text == '/help':
            self.bot.send_message(message.chat.id,
''' Привет, я люблю переносить стили и готов тебе помочь:
просто пришли мне стиль-картинку в jpg формате:) 
(с этой картинки я заберу стиль и перенесу на другую)
Также у тебя есть кнопки, подробнее в при нажатии "Помощь"''')

    def help(self, message):
        if message.text == 'Помощь':
            self.bot.send_message(message.chat.id,
'''Алгоритм успешной работы: 
                                  
1) Пришли по одиночке фотографии-стиля в формате jpg(можешь прислать сколько пожелаешь, но поодиночке)
                                  
                                  
2) Когда наберешь нужное количесвто, нажми "{ContentPic}" и пришли фотографии тоже в jpg, которые ты бы хотел разукрасить.
Тоже по одиночке( если захочешь прислать еще "стиля" то нажми "{StylePic}")
                                  
                                  
                                  
                                  
3) Можете настроить на свой вкус(попробуй их всех): \n\nРежим работы: "{All}" или "{by_parts}" 
\n\nКачество: "Изменить качество " !!!
                                  
\n\nСтепень изменения стиля: "Изменить сепень Трансформации
                                  
                                  
4)Нажми "{StartT}" для начала выполнения
                                  
                                  
                                  
5) А если захочешь все сбросить и попробывать другие картинки просто нажми "Начать заново"'''.format(
                                      ContentPic=self.contPicmode,
                                      StylePic=self.stylePicmode,
                                      StartT=self.start_message,
                                      All=self.modeAll,
                                      by_parts=self.modeByParst))

    def change_mode(self,message):
        chatid = str(message.chat.id)
        if message.text =='Главное меню':
            self.userdict[chatid]['menumode'] = 'Главное меню'
            self.bot.send_message(message.chat.id, 'Главное меню')

        if message.text =='Настройки':
            self.userdict[chatid]['menumode'] = 'Настройки'

            self.bot.send_message(message.chat.id, 'Настройки')


    def exchange_command(self, message):

        chatid = str(message.chat.id)
        greet_kb = telebot.types.ReplyKeyboardMarkup()
        self.params = [self.start_message, self.modeByParst,self.modeAll,self.stylePicmode,self.contPicmode]

        button = [telebot.types.KeyboardButton(i) for i in self.params]


        if self.userdict[chatid]['menumode'] =='Главное меню':
            greet_kb.row(button[3], button[4])
            greet_kb.row('Настройки')
            greet_kb.row(button[0])
            greet_kb.row('Начать заново')

        if self.userdict[chatid]['menumode'] == 'Настройки':
            greet_kb.row("Помощь")
            greet_kb.row('Режим трансформации')
            greet_kb.row('Изменить качество')
            greet_kb.row('Изменить степень трансформации')
            greet_kb.row('Главное меню')



        self.bot.send_message(
            message.chat.id,
            'я работаю',
            reply_markup=greet_kb
        )

    def start_again(self, message):
        chatid =  str(message.chat.id)
        if message.text == 'Начать заново':
            self.userdict[chatid]=copy.deepcopy(self.example)
            if  os.path.exists('content/content_photos/' + chatid):
                shutil.rmtree('content/content_photos/' + chatid)
            if  os.path.exists('content/style_photos/' + chatid):
                shutil.rmtree('content/style_photos/' + chatid)
            if  os.path.exists('content/final_photos/' + chatid):
                shutil.rmtree('content/final_photos/' + chatid)
            self.bot.send_message(message.chat.id, 'Все обновилость!!! Начни по-новой ')

    def inline(self,message):
        if message.text == 'Изменить качество':
            key1 = self.create_bottons([['очень низкое', 'ssS'],
                                         ['низкое', 'sS'],
                                         ['среднее', 'mS'],
                                         ['хорошее', 'MS'],
                                         ['отличное', 'SMS']])
            self.bot.send_message(message.chat.id, "ВЫБЕРИТЕ КАЧЕСТВО", reply_markup=key1)
        if message.text == 'Изменить степень трансформации':
            key2 = self.create_bottons([['очень слабая', 'ss'],
                                         ['слабая', 's'],
                                         ['средняя', 'm'],
                                         ['сильная', 'M'],
                                         ['очень сильная', 'SM']])
            self.bot.send_message(message.chat.id, "ВЫБЕРИТЕ СТЕПЕНЬ ТРАНСФОРМАЦИИ", reply_markup=key2)
        if message.text == 'Режим трансформации':
            key3 = self.create_bottons([[self.modeAll, self.modeAll],
                                         [self.modeByParst, self.modeByParst],
                                         ])
            self.bot.send_message(message.chat.id, "ВЫБЕРИТЕ РЕЖИМ ТРАНСФОРМАЦИИ", reply_markup=key3)

    def busy(self,message):
        chatid = message.chat.id
        self.bot.send_message(chatid, 'Я пока занят подсчетом')

    def repeat_all_messages(self, message):  # Название функции не играет никакой роли, в принципе
        chatid = str(message.chat.id)
        self.eho(message)
        if not self.userdict[chatid]['transfer']:
            self.help(message)
            self.inline(message)
            self.start_NST(message)

            self.take_photo(message)
            # self.photo(message)
            self.handle_docs_photo(message)
            # self.exchange_command(message)
            self.change_pic_mode(message)
            self.change_mod(message)
            self.start_again(message)
            self.prozar(message)
            #self.chooosesize(message)
            self.foridiot(message)
            self.change_mode( message)
            self.exchange_command(message)

        else:
            self.busy(message)



print("Все папки и файлы:", os.listdir('content/content_photos'))
t = ['content/content_photos/' + i for i in os.listdir('content/content_photos')]
print( os.path.exists('content/style_photos/' + "494878116/"))

print(t)
