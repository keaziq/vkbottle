import json
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader, Location, OpenLink, BaseStateGroup, CtxStorage
from vkbottle.tools.dev.mini_types.bot.message import message_min
from config import *
import requests
import datetime
from pyowm import OWM
from translate import Translator
import asyncio

ctx_storage = CtxStorage()
bot = Bot(token=token)
keyboard = Keyboard(one_time=True, inline=False)
photo_uploader = PhotoMessageUploader(bot.api)
hello = ["привет",'start','хай',]
ru_letters = "aбвгдеёжзийклмнопрстуфхцчшщъыьэюя"
en_letters = "abcdefghijklmnopqrstuvwxyz"





class Translate(BaseStateGroup):

  translator = None

class Weather(BaseStateGroup):

    city = None




@bot.on.message(text=hello)
async def message_welcome(message: Message):
    photo_up = PhotoMessageUploader(bot.api)
    photo = await photo_up.upload("menu.png")
    user = await bot.api.users.get(message.from_id)
    await message.answer(f" Здраствуйте , {user[0].first_name}."
                         f" Воспользуйтесь командой 'меню' ",attachment=photo)


@bot.on.message(text="меню")
@bot.on.message(payload={"cmd": "меню"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("Что ты умеешь?", {"cmd": "я умею"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("И что-то?", {"cmd": "2"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.row()
    keyboard.add(Location())
    keyboard.add(OpenLink("https://vk.com/club224358783", "Группа сообщества"))

    await message.answer(message="Выберай что тебе надо", keyboard=keyboard)

@bot.on.message(text="Что ты умеешь?")
@bot.on.message(payload={"cmd": "я умею"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Погода", {"cmd": "Погода"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Переводчик", {"cmd": "Переводчик"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Назад", {"cmd": "меню"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(message="Вот что я могу",keyboard=keyboard)

@bot.on.message(text=['Погода'])
async def weather(message: Message):

    await message.answer(
    message='Введите наименование города: ',
    keyboard=(
    Keyboard(one_time=True)
    .add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)
    )
    )
    await bot.state_dispenser.set(message.peer_id, Weather.city)



@bot.on.message(state=Weather.city)
async def weather_city(message:Message):
    ctx_storage.set("city", message.text)
    weather_api = OWM('e0cb111504a945363e671e0f48faf7af')
    city = ctx_storage.get("city")
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)

    manager = weather_api.weather_manager()
    observation = manager.weather_at_place(city)
    obs = observation.weather
    temp = obs.temperature('celsius')['temp']
    temp_min = obs.temperature('celsius')["temp_min"]
    temp_max = obs.temperature('celsius')["temp_max"]
    wind = obs.wind()['speed']
    humidity = obs.humidity
    pressure = obs.pressure['press']
    clouds = obs.clouds

    add_weather = (f"{city} \n Температура: {temp}℃"
          f"\n Минимальная температура: {temp_min}℃"
          f"\n Максимальная температура: {temp_max}℃"
          f"\n Ветер:{wind} м/c"
          f"\n Влажность: {humidity}%"
          f"\n Давление: {pressure} мм.рт.ст"
          f"\n Облачность: {clouds}%")

    if city is not None:
        try:
            await message.answer(add_weather, keyboard=keyboard)

        except:

            await message.answer('Не удачно', keyboard=keyboard)



@bot.on.message(text="И что-то?")
@bot.on.message(payload={"cmd": "пусто"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("пока пусто", {"cmd": "пусто"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Назад", {"cmd": "меню"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer(message="Выберай", keyboard=keyboard)



@bot.on.private_message(text=['Переводчик'])
async def note_handler(message: Message):
    text = message.text
    

@bot.on.message(state=Translate.translator) 
async def translator_text(message: Message):
    ctx_storage.set("translator",message.text)
    translator = ctx_storage.get("translator") 
    text = message.text
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)

    if text[0].lower() in ru_letters:
      translator = message
      translator = Translator(from_lang="russian", to_lang='english')

    elif text[0].lower() in en_letters:  
      translator = Translator(from_lang="english", to_lang='russian')
      
    else:

      await message.answer("Я тебя не понял")
      return
    translation = translator.translate(text)  

    if translator is not None:
      
      try:
           await message.answer translation, keyboard=keyboard)
      except:
           await message.answer('не вышло', keyboard=keyboard)
    


    # translate = Translator()
    # lang = translate.detect(message.text)
    # lang = lang.lang
    # if lang == 'ru':
    #   send = translate.translate(message.text)
    #   await message.answer(message, '------\n'+ send.text +'\n------')

    # else:
    #   send = translate.translate(message.text, dest='ru')
    #   await message.answer(message, '------\n'+ send.text +'\n------')


@bot.on.private_message(text=['пока пусто'])
@bot.on.message(payload={"cmd": "пусто"})
async def pysto(message: Message):
    await message.answer(message="пусто", keyboard=keyboard)

@bot.on.private_message()
async def noknow(message: Message):
    await message.answer(message='Я тебя не понимаю, воспользуйся командой "меню" ',)
# @bot.on.chat_message()
# async def messange_detect(messange: Message):
#     await messange.answer(messange.text)


bot.run_forever()
