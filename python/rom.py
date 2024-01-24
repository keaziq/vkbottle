from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, PhotoMessageUploader, Location, OpenLink, BaseStateGroup
from pyowm.owm import OWM


import os

bot = Bot(token="vk1.a.hHMpk86LD-qDpLrscN9vz-NV5gYnf5QIU3Cz5-tJAdZdqKP92B2c_XfAtRF5M3rcyUVtr3dl2OG0MPLEwKD0tbj2fcVYF56HCcQx7ZbMBXc8yIWhJSPb_BrJutS6wk0iWRr1_PJalVlp2QveywAdugnYmc6cVZrcfyaPtCWecyoGLGEToTioN-J8Nxc8q4Duy8mlUK--NtZxH24R7v3xxA")
keyboard = Keyboard(one_time=True, inline=False)

hello = ["привет",'start','хай',]
# ('RgKtzg6T5SDl1z3KaOaAvITQZVEXytCs')

class RegData(BaseStateGroup):

    FIND = 1

@bot.on.message(text=['Погода'])
@bot.on.message(payload={"cmd": "Погода"})
async def weather_city(message: Message):


    await message.answer(
        message='Введите наименование города: ',
        keyboard=(
            Keyboard(one_time=False, inline=False)
            .add(Text("Назад", {"cmd": "я умею"}), color=KeyboardButtonColor.NEGATIVE)
        )
    )





@bot.on.message(text=hello)
async def message_welcome(message: Message):

    user = await bot.api.users.get(message.from_id)
    await message.answer(f" Здраствуйте , {user[0].first_name}."
                         f" Воспользуйтесь командой 'меню' ")


@bot.on.message(text="меню")
@bot.on.message(payload={"cmd": "меню"})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text("Что ты умеешь?", {"cmd": "я умею"}), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("И что-то?", {"cmd": "2"}), color=KeyboardButtonColor.SECONDARY)
    keyboard. row()
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

@bot.on.chat_message(text=["/погода <city>"])
async def city_chat(message:Message, city=None):
    owm = OWM('d6901b7f0e58a81b6e3b55dc1f85fb1e')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    w = observation.weather
    temperature = w.temperature('celsius')['temp']
    weather = w.status.lower()
    wind = w.wind()['speed']
    humi = w.humidity
    if weather == "snow":
        weather = "снег"
    elif weather == "clouds":
        weather = "облачно"
    elif weather == "rain":
        weather = "дождь"

    ad = (f"По запросу города {city} найдено:\n Температура: {temperature}℃"
          f"\n Погода: {weather}\n Ветер: {wind} м/с\n Влажность: {humi}%")

    if city is not None:
        await message.answer(ad)

@bot.on.private_message()
async def noknow(message: Message):
    await message.answer(message='Я тебя не понимаю, воспользуйся командой "меню" ',)
# @bot.on.chat_message()
# async def messange_detect(messange: Message):
#     await messange.answer(messange.text)






bot.run_forever()
