import json
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from core_jarvis import CoreJarvis

jarvis = CoreJarvis()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1256967228:AAEvXSWA5ZEzcqzZi7hWWM3BVe6rLaqvFYg'

PORT = int(os.environ.get('PORT', '8443'))


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def get_duties(update, context):
    duties = json.dumps(jarvis.get_duties(), indent=2)
    update.message.reply_text(duties)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("duties", get_duties))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    """ Polling for testing purposes """
#    updater.start_polling()
 
    """ Webhook for production """
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://dumb-jarvis.herokuapp.com/" + TOKEN)
    updater.idle() 


if __name__ == '__main__':
    main()