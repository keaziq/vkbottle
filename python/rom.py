
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader, Location, OpenLink, BaseStateGroup, CtxStorage
from vkbottle.tools.dev.mini_types.bot.message import message_min
from config import *
import json
import random
import requests
from typing import Optional
import datetime
from pyowm import OWM
import goslate
from random import randint
import asyncio
from os.path import abspath as tdir
ctx_storage = CtxStorage()
bot = Bot(token=token)
keyboard = Keyboard(one_time=True, inline=False)
photo_uploader = PhotoMessageUploader(bot.api)
hello = ["привет",'start','хай','Ку-ку','здарова','здраствуйте','здраствуй']
gs = goslate.Goslate()

number_to_guess= random.randint(0,10)
is_game_started = False

class Number(BaseStateGroup):

  numbers = None


class Translate(BaseStateGroup):

  translator = None
  language = None

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
    keyboard.add(Text("Развлечение", {"cmd": "Развлечение"}), color=KeyboardButtonColor.SECONDARY)
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


@bot.on.private_message(text="Переводчик")
@bot.on.message(payload={"cmd": "язык"})
async def language(message: Message):
  key = Keyboard(one_time=True)
  key.add(Text("Русский",{"cmd":"ru"}),color=KeyboardButtonColor.POSITIVE)
  key.add(Text("English", {"cmd" : "en"}), color=KeyboardButtonColor.NEGATIVE)
  await message.answer("Выберите язык",keyboard=key)

@bot.on.private_message(text=['ru'])
@bot.on.message(payload={"cmd": "ru"})
async def ru(message: Message):
  ctx_storage.set("language", "ru")
  await message.answer("Введите текст для перевода")
  await bot.state_dispenser.set(message.peer_id, Translate.translator)

@bot.on.private_message(text=['en'])
@bot.on.message(payload={"cmd": "en"})
async def en(message: Message):
  ctx_storage.set("language", "en")
  await message.answer("Введите текст для перевода")
  await bot.state_dispenser.set(message.peer_id, Translate.translator)
  
@bot.on.message(state=Translate.translator)
@bot.on.message(payload={"cmd": "еще"})
async def translator_text(message: Message):
  ctx_storage.set("translator",message.text)
  translator = ctx_storage.get("translator") 
  language = ctx_storage.get("language")
  keyboard = Keyboard(one_time=True)
  keyboard.add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)
  keyboard.add(Text("Еще", {"cmd": "еще"}), color=KeyboardButtonColor.POSITIVE)
  if language == "ru":
    ans = gs.translate(translator, 'ru')
    await message.answer(ans,keyboard=keyboard)
    await bot.state_dispenser.delete(message.peer_id, Translate.translator)

  elif language == "en":
    ans = gs.translate(translator, 'en')
    await message.answer(ans,keyboard=keyboard)
    await bot.state_dispenser.delete(message.peer_id, Translate.translator)


@bot.on.message(text="Развлечение")
@bot.on.message(payload={"cmd": "Развлечение"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Камень,Ножницы,Бумага", {"cmd": "кнб"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Угадай число", {"cmd": "Угадай число"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Назад", {"cmd": "меню"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer(message="Выбирай", keyboard=keyboard)


@bot.on.message(text="Камень,Ножницы,Бумага")
@bot.on.message(payload={"cmd": "кнб"})
async def game_handler(message: Message):
    await message.answer("Выберите свой вариант: камень, ножницы или бумага")
  
@bot.on.message(text="камень")
@bot.on.message(text="ножницы")
@bot.on.message(text="бумага")
async def play_handler(message: Message):
  choices = ["камень", "ножницы", "бумага"]
  bot_choice = random.choice(choices)

  user_choice = message.text.lower()

  if user_choice == bot_choice:
      result = "Ничья!"
  elif (user_choice == "камень" and bot_choice == "ножницы") or (user_choice == "ножницы" and bot_choice == "бумага") or (user_choice == "бумага" and bot_choice == "камень"):
      result = "Вы победили!"
  else:
      result = "Вы проиграли!"

  await message.answer(f"Вы выбрали {user_choice}, бот выбрал {bot_choice}. {result}")


@bot.on.message(text=['Угадай число'])
@bot.on.message(payload={"cmd": "Угадай число"})
async def guess_number(message: Message):
  await message.answer("Угадай число от 1 до 100")

  number_to_guess = random.randint(1, 100)

  while True:
      response = await bot.api_ctx.messages.get_by_conversation_message_id(
          peer_id=message.peer_id,
          conversation_message_ids=[message.conversation_message_id],
      )
      user_number = int(response.items[0].text)

      if user_number < number_to_guess:
          await message.answer("Загаданное число больше")
      elif user_number > number_to_guess:
          await message.answer("Загаданное число меньше")
      else:
          await message.answer("Поздравляю, вы угадали число!")



@bot.on.private_message()
async def noknow(message: Message):
    await message.answer(message='Я тебя не понимаю, воспользуйся командой "меню" ',)

  
bot.run_forever()
