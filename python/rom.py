import json
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader, Location, OpenLink, BaseStateGroup, CtxStorage
from config import *
import requests
import datetime
from pyowm import OWM
ctx_storage = CtxStorage()
bot = Bot(token=token)
keyboard = Keyboard(one_time=True, inline=False)
photo_uploader = PhotoMessageUploader(bot.api)
hello = ["привет",'start','хай',]



class Weather(BaseStateGroup):

    city = None



@bot.on.message(text=hello)
async def message_welcome(message: Message):
    photo_up = PhotoMessageUploader(bot.api)
    photo = await photo_up.upload("D:/python/Mihaylov/photo/menu.png")
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
    keyboard.add(Text("неа", {"cmd": "нету"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Назад", {"cmd": "меню"}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer(message="Вот что я могу",keyboard=keyboard)

@bot.on.message(text=['Погода'])
@bot.on.private_message(payload={"next": "weather"})
async def weather(message: Message):

    await message.answer(
        message='Введите наименование города: ',
        keyboard=(
            Keyboard(one_time=True)
            .add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)
        )
        )
    await bot.state_dispenser.set(message.peer_id, Weather.city,  message = message)
    amount = 1


@bot.on.message(state=Weather.city)
async def weather_city(message:Message):
    ctx_storage.set("city", message.text)
    await bot.state_dispenser.delete(message.peer_id)
    weather_api = OWM('e0cb111504a945363e671e0f48faf7af')
    city = ctx_storage.get("city")
    message = message.state_peer.payload.get(" message")
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Другой город", {"next": "weather"}), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text("Назад", {"back": "start"}), color=KeyboardButtonColor.POSITIVE)

    manager = weather_api.weather_manager()
    observation = manager.weather_at_place(city)
    obs = observation.weather()
    temp = obs.get_temperature('celsius')['temp']
    wind = obs.wind()['speed']
    humidity = obs.humidity
    add_weather = (f"{city} \n Температура: {temp}℃"
          f"\n Ветер:{wind}м/c\n Влажность: {humidity}%")

    if city is not None:
        try:
            await message.answer(add_weather, keyboard=keyboard)

        except:

            await message.answer('Не удачно', keyboard=keyboard)



@bot.on.message(text="И что-то?")
@bot.on.message(payload={"cmd": "2"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("пока пусто", {"cmd": "пусто"}), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Назад", {"cmd": "меню"}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer(message="Выберай", keyboard=keyboard)



@bot.on.private_message(text=['неа'])
@bot.on.message(payload={"cmd": "нету"})
async def note(message: Message):
    await message.answer(message='Тут пока что ничего нет...',keyboard=keyboard)

@bot.on.private_message(text=['пока пусто'])
@bot.on.message(payload={"cmd": "пусто"})
async def pysto(message: Message):
    await message.answer(message='Тут пока что пусто...',)

@bot.on.private_message()
async def noknow(message: Message):
    await message.answer(message='Я тебя не понимаю, воспользуйся командой "меню" ',)
# @bot.on.chat_message()
# async def messange_detect(messange: Message):
#     await messange.answer(messange.text)


bot.run_forever()
