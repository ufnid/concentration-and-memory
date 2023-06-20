# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from random import sample
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import time
from math import floor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor, exceptions
from aiogram.types import InputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text

from functions import *
from keyboards import *


def quantity_time(n):
    itog = ""
    hours = floor((slovar_users[n]['delay'] * 60 - (time.time() - slovar_users[n]['time'])) / 3600)
    minutes = floor((slovar_users[n]['delay'] * 60 - (time.time() - slovar_users[n]['time'])) / 60 - hours)
    seconds = round(slovar_users[n]['delay'] * 60 - (time.time() - slovar_users[n]['time']) - minutes * 60 - hours * 3600)

    if hours > 0:
        itog += f'{hours} {quantity_hours(hours)}\n'
    if minutes > 0:
        itog += f'{minutes} {quantity_minutes(minutes)}\n'
    if seconds > 0:
        itog += f"{seconds} {quantity_seconds(seconds)}"
    return itog

def time_secundomer(n):
    itog = ""
    hours = floor(slovar_users[n]['time'] / 3600)
    minutes = floor(slovar_users[n]['time'] / 60) - hours * 60
    seconds = slovar_users[n]['time'] - hours * 3600 - minutes * 60
    if hours > 0:
        itog += f"{hours} {quantity_hours(hours)}\n"
    if minutes > 0:
        itog += f"{minutes} {quantity_minutes(minutes)}\n"
    if seconds > 0:
        itog += f"{seconds} {quantity_seconds(seconds)}"
    return itog

def time_tomato(n, status):
    itog = ""
    if status == 'work':
        itog += "До перерыва осталось:\n"
        minutes = floor((25 * 60 - (time.time() - slovar_users[n]['time']))/60)
        seconds = floor(25 * 60 - (time.time() - slovar_users[n]['time']) - minutes * 60)
    elif status == 'lazy':
        itog += "До конца маленького перерыва осталось:\n"
        minutes = floor((5 * 60 - (time.time() - slovar_users[n]['time']))/60)
        seconds = floor(5 * 60 - (time.time() - slovar_users[n]['time']) - minutes * 60)
    else:
        itog += "До конца большого перерыва осталось:\n"
        minutes = floor((30 * 60 - (time.time() - slovar_users[n]['time']))/60)
        seconds = floor(30 * 60 - (time.time() - slovar_users[n]['time']) - minutes * 60)

    if minutes > 0:
        itog += f"{minutes} {quantity_minutes(minutes)}\n"
    if seconds > 0:
        itog += f"{seconds} {quantity_seconds(seconds)}"

    return itog


API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


slovar_users = {}
 #                      status         targets    record           train_now                   id                                   words
#slovar_users[id] = состояние\этап, список целей, рекорд, результат тренировки сейчас, id сообщения со словами из тренировки, слова тренировки
#targets-прием целей дня, memory-слова тренировки, ready-"Запомнил", all-остальное
spis_objects = ['Стул', 'Стол', 'Кровать', 'Здание', 'Очки', 'Комод', 'Шкаф', 'Музыка', 'Курица', 'Корова', 'Кот',
                'Стена', 'Дверь', 'Розетка', 'Мышь', 'Ваза', 'Цветок', 'Бутылка', 'Вода', 'Помидор', 'Апельсин',
                'Яблоко', 'Минус', 'Число', 'Плюс', 'Рюкзак', 'Коробка', 'Камера', 'Разброс', 'Радиус', 'Диаметр']

spis_audio = ['meditation1.mp3', 'meditation2.mp3']


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!\nЯ бот для улучшения памяти и концентрации\nЧем хотите заняться?",
                         reply_markup=buttons_start, reply=False)
    if message.from_user.id not in slovar_users.keys():
        slovar_users[message.from_user.id] = dict()
        slovar_users[message.from_user.id]['status'] = 'all'
        slovar_users[message.from_user.id]['status'] = 'all'
        slovar_users[message.from_user.id]['targets'] = []
        slovar_users[message.from_user.id]['targets_output'] = []
        slovar_users[message.from_user.id]['record'] = 0
        slovar_users[message.from_user.id]['train_now'] = 3
        slovar_users[message.from_user.id]['id'] = 'msg'
        slovar_users[message.from_user.id]['words'] = ''
        slovar_users[message.from_user.id]['keyboard'] = ReplyKeyboardMarkup(resize_keyboard=True).add('Цели')
        slovar_users[message.from_user.id]['function'] = ''
        slovar_users[message.from_user.id]['function_type'] = ''
        slovar_users[message.from_user.id]['time'] = ''
        slovar_users[message.from_user.id]['delay'] = ''
        slovar_users[message.from_user.id]['tomato'] = ''


@dp.message_handler(Text(equals=['Память', 'Вернуться к меню памяти']))
async def memory(message: types.Message):
    await message.answer(
        f"Что именно интересует?\nВаш рекорд в тренировке {slovar_users[message.from_user.id]['record']}",
        reply_markup=buttons_memory, reply=False)


@dp.message_handler(Text(equals=['Как развивать память?', 'Методы запоминания', 'Как улучшить концентрацию']))
async def just_text(message: types.Message):
    match message.text:
        case "Как развивать память?":
            await message.answer(
                "Чтобы поддерживать память в тонусе, ее, как и тело, нужно тренировать. Вот несколько способов:\nИзучать иностранные языки\nРаботать над воображением и визуализацией\nНарушать автоматизм (ходить непривычной дорогой, например)\nЗапоминать фигуры (Для этого упражнения вам понадобится десять спичек. Сначала возьмите пять спичек и бросьте их на стол. В течение нескольких секунд запоминайте их расположение, потом отвернитесь и попробуйте сделать такую же картину из других пяти спичек)\nРешать арифметические примеры\nУчить стихи\nОписывать предметы\nРазгадывать кроссворды\nЗапоминать предметы или слова\nВыполнять действия вслепую\nРассказывать истории\nДелать мысленные экскурсии (Представьте себе путь на работу или мысленно прогуляйтесь по квартире)\nСтроить дворцы памяти (подробнее о них в методах запоминания)\nЗаниматься спортом\nХорошо спать\nОтслеживать количество стресса и следить за здоровьем",
                reply=False)

        case "Методы запоминания":
            await message.answer(
                "Метод локусов\nКак работает метод локусов? Представьте, что вы стоите в своем доме (дворце памяти). Мысленно пройдитесь по этому дому, запоминая его отличительные особенности — их можно использовать для хранения информации, которую вы хотите запомнить. Каждая остановка на вашем пути будет тем самым «локусом», к которому вы можете привязать идею или объект. Например, входная дверь может быть одним локусом, тумбочка в коридоре — вторым локусом, лампа в гостиной — третьим. Если вам нужно запомнить какое-то слово, создайте ассоциацию между этим словом и одним из объектов в доме. Зафиксируйте это в голове. Когда вы будете думать о своем дворце памяти, вы вспомните не только маршрут, но и объекты, привязанные к локациям\n\nМнемоника\nМнемоника основывается на образовании ассоциативных рядов и последовательностей, когда человек заменяет абстрактные объекты реальными понятиями. Главное — использовать яркие, интересные ассоциации.\nВ мнемонике можно выделить несколько наиболее известных техник:\n\nАкроним\nВы составляете комбинацию букв, которая «шифрует» полную информацию для запоминания.\nАкростих: вы придумываете стихотворение, в котором начальные буквы строк образуют какое-либо слово.\nКлючевые слова: вы выделяете во фразах ключевые слова. Вспоминая их, вы восстанавливаете в памяти всю фразу.\nРифмизация: вы придумываете рифмы, чтобы запомнить слова или цифры.\nТехника образ-имя (подходит для запоминания имен): вы придумываете любую яркую связь между именем человека и его физическими характеристиками.\nФормирование цепочки: вы сочиняете историю, в которой слово или мысль, которую нужно запомнить, вызывает цепную реакцию и тянет за собой следующие слова.\n\nЧанкинг-метод\nЭто метод подразумевает объединение нескольких элементов, которые нужно запомнить, в одну небольшую группу. Многие люди пользуются им, когда пытаются запомнить номера телефонов, номера банковских счетов, но этот метод может быть использован и для других типов информации. Чанкинг-подход часто отражается в том, как мы записываем номера телефонов — через черточку. Мы делаем это именно так, чтобы лучше воспринимать набор цифр и быстрее их запомнить.\nИнтервальные повторения\nСуть метода заключается в том, что человек повторяет выученную информацию согласно определенным, постоянно возрастающим интервалам. У этого метода даже есть конкретная формула: Y=2X+1, где Y означает день, когда информация начнет забываться, а X — день последнего повторения. Таким образом, если вы выучили информацию, например, неделю назад, то повторить ее вам нужно будет через 8 дней. При этом потенциал интервала равен бесконечности.\n\nМетод сторителлинга\nСмысл метода заключается в том, что вы создаете различные сюжетные линии, которые включают в себя элементы, необходимые для запоминания. В результате эти элементы соединяются в последовательности, и создаются истории, которые мозг лучше усваивает и воспринимает.",
                reply=False)

        case "Как улучшить концентрацию":
            await message.answer(
                "Устраните отвлекающие факторы\nУменьшите многозадачность\nПрактикуйте осознанность и медитацию\nНаладьте режим сна\nДелайте перерывы\nЧаще гуляйте на свежем воздухе\nТренируйте свой мозг\nЗанимайтесь спортом\nНекоторым помогает лёгкая музыка\nПравильно питайтесь\nСтавьте цели на день\nОбустройте рабочее место (не должно быть отвлекающих факторов, вам должно быть удобно и вы, по возможности, не должны заниматься чем то другим на этом месте)\nИспользуйте метод томата (фокусируйтесь на задаче 25 минут потом делайте перерыв 5 минут, после 4 'помидоров' сделайте перерыв 30 минут)\nИногда переключайтесь на другую задачу",
                reply=False)


@dp.message_handler(Text('Цели'))
async def targets(message: types.Message):
    if len(slovar_users[message.from_user.id]['targets']) == 0:
        await message.answer(
            'Напишите сначала число (приоритет цели, где 1 - первостепенная цель, 2 - второстепенная и т. д.), а через пробел саму цель, каждая цель должна быть в отдельном сообщении',
            reply=False, reply_markup=ReplyKeyboardMarkup())

    elif len(slovar_users[message.from_user.id]['targets']) == 1:
        await message.answer(
            f"Ваши цели:\n{slovar_users[message.from_user.id]['targets_output']}\n\nЧтобы удалить цель из списка, нажмите на соответствующую кнопку",
            reply=False, reply_markup=slovar_users[message.from_user.id]['keyboard'])

    else:
        await message.answer(
            f"Ваши цели:\n{slovar_users[message.from_user.id]['targets_output']}\n\nЧтобы удалить цель из списка, нажмите на соответствующую кнопку",
            reply=False, reply_markup=slovar_users[message.from_user.id]['keyboard'])
    slovar_users[message.from_user.id]['status'] = 'targets'


@dp.message_handler(Text(equals=['Тренировка', 'Попробовать ещё раз']))
async def training_words(message: types.Message):
    await message.answer(
        "Запомните и напишите как можно больше предметов, тренировка продолжается пока вы не ошибетесь.\nКогда запомните слова - нажмите 'Запомнил', потом пишите сами слова через пробел, регистр не важен",
        reply=False)
    output = " ".join(sample(spis_objects, slovar_users[message.from_user.id]['train_now']))
    slovar_users[message.from_user.id]['words'] = output
    slovar_users[message.from_user.id]['id'] = await message.answer(output, reply=False, reply_markup=button_zapomnil)
    slovar_users[message.from_user.id]['status'] = 'ready'


@dp.message_handler(Text(equals=['Концентрация', 'Вернуться к меню концентрации']))
async def concentration_menu(message: types.Message):
    await message.answer(
        "Что именно интересует?",
        reply_markup=buttons_conc, reply=False)


@dp.message_handler(Text(equals=['Таймер', 'Проверить сколько еще осталось']))
async def timer(message: types.Message):
    if slovar_users[message.from_user.id]['function_type'] == 'timer':
        try:
            await message.answer(
                f"До конца таймера:\n{quantity_time(message.from_user.id)}",
                reply_markup=timer_buttons, reply=False)
        except:
            await message.answer(
                f"Время уже вышло",
                reply_markup=buttons_conc, reply=False)
            slovar_users[message.from_user.id]['function_type'] = ''
    else:
        await message.answer(
            "Напишите на сколько минут поставить таймер или нажмите на кнопку для перехода в соответствующий раздел",
            reply_markup=buttons_conc, reply=False)
        slovar_users[message.from_user.id]['status'] = 'timer'


@dp.message_handler(Text(equals=['Секундомер', 'Проверить сколько уже прошло']))
async def secundomer(message: types.Message):
    if slovar_users[message.from_user.id]['function_type'] == 'secundomer':
        await message.answer(
            f"Секундомер работает уже {time_secundomer(message.from_user.id)}",
            reply_markup=secundomer_buttons_working, reply=False)
    else:
        await message.answer(
            "Выберите что вы хотите сделать",
            reply_markup=secundomer_buttons, reply=False)


@dp.message_handler(Text('Остановить таймер'))
async def stop_timer(message: types.Message):
     try:
        slovar_users[message.from_user.id]['function'].cancel()
        slovar_users[message.from_user.id]['function_type'] = ''
        await message.answer(
            f"Таймер остановлен, оставалось:\n{quantity_time(message.from_user.id)}\n\nНапишите на сколько минут поставить новый таймер или нажмите на кнопку для перехода в соответствующий раздел",
            reply_markup=buttons_conc, reply=False)

     except:
        await message.answer(
            "Время уже и так вышло",
            reply_markup=buttons_conc, reply=False)
        slovar_users[message.from_user.id]['function_type'] = ''


@dp.message_handler(Text('Остановить секундомер'))
async def stop_secundomer(message: types.Message):
    slovar_users[message.from_user.id]['function'].cancel()
    slovar_users[message.from_user.id]['function_type'] = ''
    await message.answer(f"Отсчёт окончен, вот сколько времени прошло:\n{time_secundomer(message.from_user.id)}",
        reply=False)


@dp.message_handler(Text('Запустить секундомер'))
async def start_secundomer(message: types.Message):
    if slovar_users[message.from_user.id]['function_type'] == 'secundomer':
        await message.answer(
            f"Отсчёт секундомера окончен, вот сколько времени прошло:\n{time_secundomer(message.from_user.id)}",
            reply=False)
    elif slovar_users[message.from_user.id]['function_type'] == 'timer':
        try:
            await message.answer(
                f"Предыдущий таймер остановален, оставалось:\n{quantity_time(message.from_user.id)}",
                reply=False)
        except:
            pass

    async def secundomer(n):
        slovar_users[n]['time'] = 0
        slovar_users[n]['function_type'] = 'secundomer'
        while True:
            await asyncio.sleep(1)
            slovar_users[n]['time'] += 1


    slovar_users[message.from_user.id]['function'] = asyncio.create_task(secundomer(message.from_user.id))
    slovar_users[message.from_user.id]['function_type'] = 'secundomer'
    slovar_users[message.from_user.id]['function']
    await message.answer(f"Секундомер запущен",
                         reply=False, reply_markup=secundomer_buttons_working)


@dp.message_handler(Text(equals=['Метод томата', "Проверить сколько осталось работать/отдыхать"]))
async def tomato(message: types.Message):
    if slovar_users[message.from_user.id]['function_type'] == 'tomato':
        await message.answer(
            f"{time_tomato(message.from_user.id, slovar_users[message.from_user.id]['tomato'])}",
            reply_markup=tomato_buttons_working, reply=False)

    else:
        await message.answer(
            f"Если не знаете что это за метод, можете посетите конец раздела 'Как улучшить концентрацию', если же знаете, то выберете действие",
            reply_markup=tomato_buttons, reply=False)


@dp.message_handler(Text('Запустить метод томата'))
async def tomato_working(message: types.Message):
    if slovar_users[message.from_user.id]['function_type'] == 'secundomer':
        await message.answer(
            f"Отсчёт секундомера окончен, вот сколько времени прошло:\n{time_secundomer(message.from_user.id)}",
            reply=False)
    elif slovar_users[message.from_user.id]['function_type'] == 'timer':
        try:
            await message.answer(
                f"Предыдущий таймер остановален, оставалось:\n{quantity_time(message.from_user.id)}",
                reply=False)
        except:
            pass

    async def tomato_start(n):
        await message.answer(
            'Метод томата запущен', reply=False, reply_markup=tomato_buttons_working)
        while True:
            for i in range(4):
                await message.answer(
                    'Пора работать', reply=False, reply_markup=tomato_buttons_working)
                slovar_users[n]['tomato'] = 'work'
                slovar_users[n]['time'] = time.time()
                await asyncio.sleep(25 * 60)
                if i != 3:
                    await message.answer(
                        'Время перерыва', reply=False, reply_markup=tomato_buttons_working)
                    slovar_users[n]['tomato'] = 'lazy'
                    slovar_users[n]['time'] = time.time()
                    await asyncio.sleep(5 * 60)

                else:
                    await message.answer(
                        'Время большого перерыва', reply=False, reply_markup=tomato_buttons_working)
                    slovar_users[n]['tomato'] = 'big lazy'
                    slovar_users[n]['time'] = time.time()
                    await asyncio.sleep(30 * 60)


    slovar_users[message.from_user.id]['function_type'] = 'tomato'
    slovar_users[message.from_user.id]['function'] = asyncio.create_task(tomato_start(message.from_user.id))
    slovar_users[message.from_user.id]['function']


@dp.message_handler(Text('Остановить метод томата'))
async def tomato_stop(message: types.Message):
    slovar_users[message.from_user.id]['function'].cancel()
    slovar_users[message.from_user.id]['function_type'] = ''
    await message.answer(
        "Метод томата выключен",
        reply=False, reply_markup=tomato_buttons)


@dp.message_handler(Text(equals=['Медитация', 'Ещё аудио']))
async def meditation(message: types.Message):
    await message.answer(
        "Это может занять некоторое время, пожалуйста, подождите",
        reply=False, reply_markup=ReplyKeyboardRemove())
    file = sample(spis_audio, k=1)
    audio = open(file[0], 'rb')
    await bot.send_audio(message.from_user.id, audio)
    audio.close()
    await message.answer(
        "Медитируйте пока играет музыка",
        reply=False, reply_markup=meditation_buttons)


@dp.message_handler()
async def send_other(message: types.Message):
    match slovar_users[message.from_user.id]['status']:
        case "ready":
            await slovar_users[message.from_user.id]['id'].delete()
            slovar_users[message.from_user.id]['status'] = "memory"

        case "memory":
            if slovar_users[message.from_user.id]['words'].lower() == message.text.lower():
                slovar_users[message.from_user.id]['train_now'] += 1
                output = " ".join(sample(spis_objects, slovar_users[message.from_user.id]['train_now']))
                slovar_users[message.from_user.id]['words'] = output
                slovar_users[message.from_user.id]['id'] = await message.answer(output, reply_markup=button_zapomnil,
                                                                                reply=False)
                slovar_users[message.from_user.id]['status'] = "ready"
            else:
                if slovar_users[message.from_user.id]['train_now'] == 3:
                    await message.answer(
                        f"Неправильно\nНе огорчайтесь, вы ведь ещё учитесь",
                        reply_markup=training, reply=False)

                elif slovar_users[message.from_user.id]['train_now'] == slovar_users[message.from_user.id]['record']:
                    if slovar_users[message.from_user.id]['record'] != 0:
                        await message.answer(
                            f"Неправильно, вы смогли запомнить {slovar_users[message.from_user.id]['train_now'] - 1} {quantity_words(slovar_users[message.from_user.id]['train_now'] - 1)}, ваш рекорд - {slovar_users[message.from_user.id]['record']}\nВы дошли до своего предыдущего рекорда, неплохо!",
                            reply_markup=training, reply=False)
                    else:
                        await message.answer(
                            f"Неправильно, вы смогли запомнить {slovar_users[message.from_user.id]['train_now'] - 1} {quantity_words(slovar_users[message.from_user.id]['train_now'] - 1)}\nВсегда можно попробовать ещё раз",
                            reply_markup=training, reply=False)
                elif slovar_users[message.from_user.id]['train_now'] > slovar_users[message.from_user.id]['record']:
                    if slovar_users[message.from_user.id]['record'] != 0:
                        await message.answer(
                            f"Неправильно, вы смогли запомнить {slovar_users[message.from_user.id]['train_now'] - 1} {quantity_words(slovar_users[message.from_user.id]['train_now'] - 1)}, ваш рекорд - {slovar_users[message.from_user.id]['record']}\nВау! Вы побили свой рекорд! Можете собой гордиться",
                            reply_markup=training, reply=False)
                    else:
                        await message.answer(
                            f"Неправильно, вы смогли запомнить {slovar_users[message.from_user.id]['train_now'] - 1} {quantity_words(slovar_users[message.from_user.id]['train_now'] - 1)}",
                            reply_markup=training, reply=False)
                    slovar_users[message.from_user.id]['record'] = slovar_users[message.from_user.id]['train_now'] - 1
                else:
                    await message.answer(
                        f"Неправильно, вы смогли запомнить {slovar_users[message.from_user.id]['train_now'] - 1}, ваш рекорд - {slovar_users[message.from_user.id]['record']}\nУверен, в следующий раз будет лучше, не отчаивайтесь!",
                        reply_markup=training, reply=False)
                slovar_users[message.from_user.id]['train_now'] = 3
                slovar_users[message.from_user.id]['status'] = 'all'

        case 'targets':
            try:
                slovar_users[message.from_user.id]['targets'].remove([int(message.text.split(' ')[0]), ' '.join(message.text.split(' ')[1:])])   #если есть такая цель в списке - удаляю

                slovar_users[message.from_user.id]['keyboard'] = ReplyKeyboardMarkup(resize_keyboard=True).add('Цели')
                slovar_users[message.from_user.id]['targets_output'] = slovar_users[message.from_user.id]['targets'][:]
                for i in range(len(slovar_users[message.from_user.id]['targets_output'])):
                    slovar_users[message.from_user.id]['targets_output'][i] = slovar_users[message.from_user.id]['targets'][i][:]
                    slovar_users[message.from_user.id]['targets_output'][i][0] = str(slovar_users[message.from_user.id]['targets_output'][i][0])
                    slovar_users[message.from_user.id]['targets_output'][i] = ' '.join(slovar_users[message.from_user.id]['targets_output'][i])
                for i in slovar_users[message.from_user.id]['targets_output']:
                    slovar_users[message.from_user.id]['keyboard'].add(i)
                slovar_users[message.from_user.id]['targets_output'] = '\n'.join(slovar_users[message.from_user.id]['targets_output'])

                await message.answer(f"цель '{' '.join(message.text.split(' ')[1:])}' удалена из списка", reply_markup=slovar_users[message.from_user.id]['keyboard'])
            except:
                slovar_users[message.from_user.id]['targets'].append([int(message.text.split(' ')[0]), ' '.join(message.text.split(' ')[1:])])   #иначе добавляю и сортирую список
                slovar_users[message.from_user.id]['targets'].sort(key=lambda x: x[0])

                slovar_users[message.from_user.id]['keyboard'] = ReplyKeyboardMarkup(resize_keyboard=True).add('Цели')
                slovar_users[message.from_user.id]['targets_output'] = slovar_users[message.from_user.id]['targets'][:]
                for i in range(len(slovar_users[message.from_user.id]['targets_output'])):
                    slovar_users[message.from_user.id]['targets_output'][i] = slovar_users[message.from_user.id]['targets'][i][:]
                    slovar_users[message.from_user.id]['targets_output'][i][0] = str(slovar_users[message.from_user.id]['targets_output'][i][0])
                    slovar_users[message.from_user.id]['targets_output'][i] = ' '.join(slovar_users[message.from_user.id]['targets_output'][i])
                for i in slovar_users[message.from_user.id]['targets_output']:
                    slovar_users[message.from_user.id]['keyboard'].add(i)
                slovar_users[message.from_user.id]['targets_output'] = '\n'.join(slovar_users[message.from_user.id]['targets_output'])

                await message.answer(f"цель '{' '.join(message.text.split(' ')[1:])}' добавлена в список", reply_markup=slovar_users[message.from_user.id]['keyboard'])

        case 'all':
            await message.answer(f"Я не понимаю(")

        case 'timer':
            async def timer_start(delay, n):
                slovar_users[n]['time'] = time.time()
                await asyncio.sleep(delay * 60)
                slovar_users[n]['function_type'] = ''
                slovar_users[n]['status'] = 'all'
                await message.answer('Время вышло',
                    reply=False)

            if slovar_users[message.from_user.id]['function_type'] == 'secundomer':
                await message.answer(
                    f"Отсчёт секундомера окончен, вот сколько времени прошло:\n{time_secundomer(message.from_user.id)}",
                    reply=False)
            elif slovar_users[message.from_user.id]['function_type'] == 'timer':
                try:
                    await message.answer(
                        f"Предыдущий таймер остановален, оставалось:\n{quantity_time(message.from_user.id)}",
                        reply=False)
                except:
                    pass

            slovar_users[message.from_user.id]['delay'] = int(message.text)
            slovar_users[message.from_user.id]['function'] = asyncio.create_task(timer_start(int(message.text), message.from_user.id))
            slovar_users[message.from_user.id]['function_type'] = 'timer'
            slovar_users[message.from_user.id]['function']
            await message.answer('Таймер запущен',
                reply_markup=timer_buttons, reply=False)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


#Медитация, секундомер, таймер, томат