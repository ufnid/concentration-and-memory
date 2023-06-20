def quantity_words(n):
    if n in range(5, 21):
        return 'слов'

    elif str(n)[-1] == '1':
        return 'слово'

    elif str(n)[-1] in map(str, range(2, 5)):
        return 'слова'

    else:
        return 'слов'


def quantity_hours(n):
    if n in range(5, 21):
        return 'часов'

    elif str(n)[-1] == '1':
        return 'час'

    elif str(n)[-1] in map(str, range(2, 5)):
        return 'часа'

    else:
        return 'часов'


def quantity_minutes(n):
    if n in range(5, 21):
        return 'минут'

    elif str(n)[-1] == '1':
        return 'минута'

    elif str(n)[-1] in map(str, range(2, 5)):
        return 'минуты'

    else:
        return 'минут'


def quantity_seconds(n):
    if n in range(5, 21):
        return 'секунд'

    elif str(n)[-1] == '1':
        return 'секунду'

    elif str(n)[-1] in map(str, range(2, 5)):
        return 'секунды'

    else:
        return 'секунд'