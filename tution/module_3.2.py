import re

def send_email(recepient, message, sender = 'university.help@gmail.com'):
    dog = "@"
    if not dog in sender or not dog in recepient or not sender.endswith(('.com', '.ru', '.net'))  or not recepient.endswith(('.com', '.ru', '.net')):
        print('Невозможно отправить письмо с адреса ', sender, 'на адрес', recepient)
        return
    if recepient == sender:
        print('Нельзя отправить письмо самому себе!')
        return
    if sender != 'university.help@gmail.com':
        print('НЕСТАНДАРТНЫЙ ОТПРАВИТЕЛЬ! Письмо отправлено с адреса ', sender, 'на адрес ', recepient)
        return

    print('Письмо успешно отправлено с адреса ', sender, 'на адрес', recepient)

send_email('epyur@ya.ru', 'text')