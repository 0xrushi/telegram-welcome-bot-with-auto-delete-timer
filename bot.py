import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Chat
from telegram.ext.dispatcher import run_async
import logging
from time import sleep

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "" # get token from command-line


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def referpinned(bot,update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('rpin.jpg', 'rb'))

# Welcomes the new member of the group
@run_async
def welcomemessage(bot, update):
    msg = update.message
    bot.send_message(chat_id=msg.chat_id, text=f'Hey <a href="tg://user?id={msg.new_chat_members[0].id}">{msg.new_chat_members[0].first_name}</a>, Welcome to this group. We are grateful to have you as a part of us.Refer the pinned post for more resources and rules.', parse_mode='HTML')
    #print(update)
    #print(msg.message_id)
    #print(msg.chat.id)
    bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id) # Deletes the "'NAME' joined the group"
    sleep(600)
    bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id+1) # Deletes Hello $user welcome to the group message
    #print(update.message.message_id)

# Deletes a the left group message
@run_async
def deleteleft(bot, update):
    msg = update.message
    bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)

def main():
    updater = Updater(TOKEN)
    bot = updater.bot
    dispatcher = updater.dispatcher
    job = dispatcher.job_queue
    # Handlers Filters.status_update.new_chat_members
    welcomemessage_handler = MessageHandler(Filters.status_update.new_chat_members, welcomemessage)
    deleteleft_handler = MessageHandler(Filters.status_update.left_chat_member, deleteleft)

    # Dispatchers
    dispatcher.add_handler(CommandHandler("refer_pinned", referpinned))

    dispatcher.add_handler(welcomemessage_handler)
    dispatcher.add_handler(deleteleft_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
