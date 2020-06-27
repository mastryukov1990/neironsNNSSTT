from NewBot import BBB
from config import data_for_bot
from telebot import types
def start():
    mybot = BBB(data_for_bot)




    @mybot.bot.message_handler(content_types=["text",'photo'])
    def inline(message):
       mybot.repeat_all_messages(message)
    @mybot.bot.callback_query_handler(func=lambda c: True)
    def inline(c):
        chatid = str(c.message.chat.id)
        mybot.chooosesizeC(c)
        mybot.prozarC(c)

    mybot.bot.polling()
start()