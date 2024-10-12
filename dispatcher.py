import asyncio
import math
import os
import requests
from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.types import Message
from dotenv import load_dotenv
from pydantic_core._pydantic_core import ValidationError

load_dotenv()

class CheckWeather(StatesGroup):
    location = State()

class BotTelegram:
    def __init__(self, token_from_telegram):
        self.bot = BotMessage(token_from_telegram)
        self.dispatcher = DispatcherMessage(self.bot)

    async def start_dispatcher(self):
        await self.dispatcher.start_polling(self.bot)

    def run(self):
        asyncio.run(self.start_dispatcher())


class BotMessage(Bot):
    def __init__(self, token, **kw):
        Bot.__init__(self, token, **kw)


class DispatcherMessage(Dispatcher):
    def __init__(self, bot, **kw):
        Dispatcher.__init__(self, **kw)

        @self.message(Command('start'))
        async def start_message(message:Message, state:FSMContext):
            await message.answer('Привет! Я бот, для выполнения тестового задания от Bobr Ai!\n'
                                 'Я умею показывать температуру, влажность, давление в зависиомости от введенного метстоположения\n'
                                 'Давай попробуем! Введи название города для проверки!')
            await state.set_state(state=CheckWeather.location)

        @self.message()
        async def check_weather(message:Message, state:FSMContext):
            await state.update_data(location=message.text)
            data = await state.get_data()
            location = data['location']
            try:
                url = os.environ['URL_part1'] + str(location).lower() + os.environ['URL_part2']+os.environ['API_KEY']
                weather_data = requests.get(url).json()
                temperature = round(weather_data['main']['temp'])
                pressure = math.ceil(weather_data['main']['pressure']/1.333)
                humidity = round(weather_data['main']['humidity'])
                temperature_feels = round(weather_data['main']['feels_like'])
                await message.reply('Сейчас в городе ' +str(location)+ ' ' + str(temperature) + ' °C,\n'
                                    'Ощущается как ' +  str(temperature_feels) + ' °C,\n'
                                    'Влажность ' + str(humidity) + '%, \n'
                                    'Давление ' + str(pressure) + ' мм рт. ст.\n')
            except ValidationError as exc:
                print(repr(exc.errors()[0]['type']))
                await message.reply('Произошла ошибка, проверьте название города!')