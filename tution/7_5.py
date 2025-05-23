"""
Переменные: количество участников первой команды (team1_num).
Пример итоговой строки: "В команде Мастера кода участников: 5 ! "
"""
team1_num = 5
print("В команде Мастера кода участников: %s!" % team1_num)

"""
Переменные: количество участников в обеих командах (team1_num, team2_num).
Пример итоговой строки: "Итого сегодня в командах участников: 5 и 6 !"
"""

team2_num = 6
print("В команде Мастера кода участников: %s и %s!" % (team1_num, team2_num))

"""
Использование format():

Переменные: количество задач решённых командой 2 (score_2).
Пример итоговой строки: "Команда Волшебники данных решила задач: 42 !"
"""
score_1 = 40

score_2 = 42
print("Команда Волшебники данных решила задач: {}!".format(score_2))
'''
Переменные: время за которое команда 2 решила задачи (team1_time).
Пример итоговой строки: " Волшебники данных решили задачи за 18015.2 с !"
'''
team1_time = 1552.512

team2_time = 2153.31451
print("Волшебники данных решили задачи за {}с !".format(score_2*team2_time))
'''
Использование f-строк:

Переменные: количество решённых задач по командам: score_1, score_2
Пример итоговой строки: "Команды решили 40 и 42 задач.”
'''
print(f'Команды решили {score_1} и {score_2} задач.')
tasks_total = 82

time_avg = 45.2

challenge_result = 'Победа команды Волшебники данных!'

'''Переменные: исход соревнования (challenge_result).
Пример итоговой строки: "Результат битвы: победа команды Мастера кода!"
'''
print(f'Результат битвы: {challenge_result}!')

'''Переменные: количество задач (tasks_total) и среднее время решения (time_avg).
Пример итоговой строки: "Сегодня было решено 82 задач, в среднем по 350.4 секунды на задачу!."
'''
print(f'Сегодня было решено {tasks_total} задач, в среднем по {time_avg} секунды на задачу!')










