from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from token_bot import TOKEN
from api_weather import API
import requests
import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


#CREATE CONST

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage = storage)


#SQL

def date_base():
  global db, cur
  db = sqlite3.connect('main_city.db')
  cur = db.cursor()
  if db:
    print('[!]Data base been connected!')
  cur.execute("""
    CREATE TABLE IF NOT EXISTS menu(
      ids INT,
      city TEXT
    )
  """)
  db.commit()

async def add_info(state):
  async with state.proxy() as data:
    cur.execute('INSERT INTO menu VALUES (?, ?)', tuple(data.values()))
    db.commit()


#machine state
class Admin(StatesGroup):
  ids = State()
  city = State()

@dp.message_handler(commands = 'Choice_my_city', state = None)
async def get_all(message: types.Message):
  await Admin.ids.set()
  await message.answer("Enter u'r city", reply_markup = kb_rem)

@dp.message_handler(state = Admin.ids)
async def get_id(message: types.Message, state = FSMContext):
  async with state.proxy() as data:
    data['id'] = message.from_user.id
  await Admin.next()
  await message.answer("Enter u'r city again for confirmation")

@dp.message_handler(state = Admin.city)
async def get_city(message: types.Message, state: FSMContext):
  async with state.proxy() as data: 
    data['city'] = message.text
  await add_info(state)
  await state.finish()
  await message.answer("U'r city been registr!", reply_markup = kb_reg)
  
#statr

@dp.message_handler(commands = 'start')
async def start(message: types.Message):
  cur.execute('SELECT ids FROM menu')
  if cur.fetchone() is None:
    await message.answer('Hello, welcome to the weather bot! Use the keyboard to control the bot!', reply_markup = kb)
  else:
    await message.answer('Hello, welcome to the weather bot! Use the keyboard to control the bot!', reply_markup = kb_reg)


@dp.message_handler(commands = 'Get_weather')
async def weather(message: types.Message):
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

@dp.message_handler(commands = 'Cheak_into_my_city')
async def into_city(message: types.Message):
  id_user = message.from_user.id
  cur.execute(f'SELECT city FROM menu WHERE ids = "{id_user}"')
  city_user = cur.fetchone()
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
      print(city_user[0])
      r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_user[0]}&appid={API}&units=metric')
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
      await message.answer(f'***{time_now}***\nSity: {city_user[0]}\nTemp: {temp_sity} C° {wd}\nHumidity: {humidity}\nSunup: {sunup}\nSundown: {sundown}\nWind: {wind} m/s\n***Have a good day***')
  except:
      await message.answer('\U00002620Error! Cheack name city!\U00002620')


@dp.message_handler(commands = 'Exit')
async def quit(message: types.Message):
  await message.answer("Oh come on, don't forget to check back tomorrow!", reply_markup = kb_rem)

#@dp.message_handler()


#keyboard

kb = ReplyKeyboardMarkup(resize_keyboard = True)
kb_reg = ReplyKeyboardMarkup(resize_keyboard = True)
kb_rem = ReplyKeyboardRemove()
b1 = KeyboardButton('/Get_weather')
b2 = KeyboardButton('/Choice_my_city')
b3 = KeyboardButton('/Cheak_into_my_city')
b4 = KeyboardButton('/Exit')

kb.add(b1).add(b2).add(b4)
kb_reg.add(b1).add(b3).add(b4)


#start 

async def start_message(_):
    print('[!]Bot been started!')
    date_base()


#EXECUTOR

executor.start_polling(dp, skip_updates = True, on_startup = start_message)
