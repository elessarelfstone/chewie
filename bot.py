import logging

from telegram import Bot
from telegram import File
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters

from handlers import transcript_file_upload_handler
from settings import TOKEN


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_message_handler(update, context):
    user = update.message.from_user
    if user:
        name = user.first_name
    else:
        name = 'anonim'

    text = update.message.text
    reply_text = f'Привет, {name}! \n\n{text}'
    bot = context.bot

    update.message.reply_text(reply_text)
    # bot.send_message(chat_id=update.effective_message.chat_id,
    #                  text=reply_text)


def main():

    print("start")
    updater = Updater(TOKEN, use_context=True)
    # handler = MessageHandler(Filters.all, test_message_handler)
    test_handler = MessageHandler(Filters.document, transcript_file_upload_handler)

    # updater.dispatcher.add_handler(handler)
    updater.dispatcher.add_handler(test_handler)
    updater.start_polling()
    updater.idle()
    print("finish")


if __name__ == '__main__':
    main()
