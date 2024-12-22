import random
from itertools import count


def quiz():
    numbers = range(3, 21)
    control = random.choice(numbers)
    return control
choice = quiz()

control_number = range(1, choice)
control_number2 = []

for n in control_number:
    control_number2.append(n)

if choice % 2 != 0:
    long = len(control_number2)
    half_long = int(long / 2)
    del control_number2[half_long:]

if choice % 2 == 0:
    long2 = len(control_number2)
    half_long2 = int(long2 / 2) + 1
    del control_number2[half_long2:]

control_list = []

for i in control_number2:
    if choice % i == 0:
        control_list.append(i)
        continue
control_list.append(choice)

control_list.remove(1)
if control_list.count(2):
    control_list.remove(2)

password_list = []


for p in control_number2:
    for q in control_list:
        if p < q - p:
            password_list.append((p, q - p))



print("Случайное число:", choice)
print("Контрольная последовательность: ", *password_list)



