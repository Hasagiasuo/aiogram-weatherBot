from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from token_bot import TOKEN
from api_weather import API
import requests
import datetime


#GET WEATHER

#def get_weather(city, API):


#CREATE CONST

bot = Bot(TOKEN)
dp = Dispatcher(bot)


#EVERY TIME

@dp.message_handler(commands = 'start')
async def echo(message: types.Message):
    await message.answer('Enter city and i`ll resend u inforamtion!')

@dp.message_handler()
async def get_weather(message: types.Message):
  code_to_smile = {
    'Clear': 'Sun \U0001F31E',
    'Clouds': 'Clounds \U00002601',
    'Rain': 'Rain \U0001F327',
    'Brizzle': 'Brizzle \U0001F326',
    'Thundersthorm': 'Thundershtorm \U0001F329',
    'Snow': 'Snow \U0001F328',
    'Mist': 'Mist \U0001F32B'
  }

  try:
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API}&units=metric')
    data = r.json()
    type_weather = data['weather'][0]['main']
    temp_sity = data['main']['temp']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    sunup = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sundown = datetime.datetime.fromtimestamp(data['sys']['sunset'])
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')
    if type_weather in code_to_smile:
      wd = code_to_smile[type_weather]
    else:
      wd = 'Just look into window, i can`t know!'
    await message.answer(f'***{time_now}***\nSity: {message.text}\nTemp: {temp_sity} C° {wd}\nHumidity: {humidity}\nSunup: {sunup}\nSundown: {sundown}\nWind: {wind} m/s\n***Have a good day***')
  except:
    await message.answer('\U00002620Error! Cheack name city!\U00002620')

#EXECUTOR

executor.start_polling(dp, skip_updates = True)