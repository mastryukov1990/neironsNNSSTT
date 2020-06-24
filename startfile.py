from Bottry import BBB
from config import data_for_bot
mybot = BBB(data_for_bot)
@mybot.bot.message_handler(content_types=["text", 'photo','command'])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    mybot.repeat_all_messages(message)


mybot.bot.polling()