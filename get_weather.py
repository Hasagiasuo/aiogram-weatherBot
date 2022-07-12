from api_weather import API
import requests
from pprint import pprint
import datetime

def get_weather(sity, API):

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
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={sity}&appid={API}&units=metric')
    data = r.json()
    #pprint(data)
    type_weather = data['weather'][0]['main']
    city = data['name']
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
    print(f'***{time_now}***\nSity: {city}\nTemp: {temp_sity} C° {wd}\nHumidity: {humidity}\nSunup: {sunup}\nSundown: {sundown}\nWind: {wind} m/s')
  except Exception as error:
    print('[!]Error {error}!\nCheack name city!')

def main():
  sity = input('[*]Enter city: ')
  get_weather(sity, API)

if __name__ == '__main__':
  main()