from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

# Пользователь нажал start
buttons_start = ReplyKeyboardMarkup(resize_keyboard=True).add("Память").add("Концентрация").add("Цели")
# Выбрал память
buttons_memory = ReplyKeyboardMarkup(resize_keyboard=True).add("Как развивать память?").add("Методы запоминания").add("Тренировка")
# Запомнил
button_zapomnil = ReplyKeyboardMarkup(resize_keyboard=True).add('Запомнил')
# Концентрация
buttons_conc = ReplyKeyboardMarkup(resize_keyboard=True).add("Как улучшить концентрацию").add("Медитация").add("Таймер").add("Секундомер").add("Метод томата")
#После тренировки
training = ReplyKeyboardMarkup(resize_keyboard=True).add("Попробовать ещё раз").add("Вернуться к меню памяти")
#Таймер
timer_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add("Остановить таймер").add('Проверить сколько еще осталось').add("Вернуться к меню концентрации")
#Секундомер не запущен
secundomer_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add("Запустить секундомер").add("Вернуться к меню концентрации")
#Секундомер запущен
secundomer_buttons_working = ReplyKeyboardMarkup(resize_keyboard=True).add("Остановить секундомер").add('Проверить сколько уже прошло').add("Вернуться к меню концентрации")
#Томат не запущен
tomato_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add("Запустить метод томата").add("Вернуться к меню концентрации")
#Томат  запущен
tomato_buttons_working = ReplyKeyboardMarkup(resize_keyboard=True).add("Остановить метод томата").add("Проверить сколько осталось работать/отдыхать").add("Вернуться к меню концентрации")
#Медитация
meditation_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add("Ещё аудио").add("Вернуться к меню концентрации")