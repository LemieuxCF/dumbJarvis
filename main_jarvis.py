from datetime import datetime, timedelta
import logging
import os
import pytz
from telegram.ext import (
    CommandHandler, 
    Dispatcher, 
    Filters,
    Job,
    JobQueue, 
    MessageHandler, 
    Updater
)
from core_jarvis import CoreJarvis

jarvis = CoreJarvis()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = ''

PORT = int(os.environ.get('PORT', '8443'))


class DumbJarvis:
    def __init__(self, mode = 'test', timezone = 'Asia/Seoul'):
        """ Initialize mode: default is test, 'prod' for production 
            and timezone: default is Asia/Seoul             
        """
        self.__mode = mode
        self.__timezone = timezone

        """ Initialize core Python telegram API objects """
        self.__updater: Updater = Updater(TOKEN, use_context = True)
        self.__dp: Dispatcher = self.__updater.dispatcher
        self.__job_queue: JobQueue = self.__updater.job_queue
        
        """ Initialize core functionality object """
        self.__jarvis: CoreJarvis = CoreJarvis()

        """ Declare periodic jobs """
        self.__duties_job: Job = None

        """ Add handlers """
        self.__dp.add_handler(CommandHandler("start", self.__start))
        self.__dp.add_handler(CommandHandler("duties", self.__get_duties))
        self.__dp.add_handler(MessageHandler(Filters.text, self.__echo))


    def run(self):
        if (self.__mode == 'test'):
            self.__updater.start_polling() 
        else:
            self.__updater.start_webhook(listen="0.0.0.0",
                         port=PORT,
                         url_path=TOKEN)
            self.__updater.bot.set_webhook("https://dumb-jarvis.herokuapp.com/" + TOKEN)
            self.__updater.idle() 
           

    def __start(self, update, context):
        """ Start the duties reminder job """
        self.__duties_job = self.__job_queue.run_repeating(
            self.__update_and_release_duties,
            timedelta(seconds=20),
            pytz.timezone(self.__timezone).localize(
                datetime(2020, 4, 29, 3, 15, 0)))
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi there!')

    def __echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def __get_duties(self, update, context):
        update.message.reply_text(jarvis.get_duties())

    def __update_and_release_duties(self, context):
        jarvis.update_duties()
        context.bot.send_message(chat_id='221220492', 
            text=""" Duties updated for this week:
            {0} """.format(jarvis.get_duties()))


def main():
    dumb_jarvis = DumbJarvis()
    dumb_jarvis.run()
    

if __name__ == '__main__':
    main()
