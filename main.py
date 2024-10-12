import os
from dispatcher import BotTelegram
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    bot = BotTelegram(os.environ["BOT_TOKEN"])
    bot.run()
