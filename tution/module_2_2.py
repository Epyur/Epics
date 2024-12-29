first = int(input("Input first number: "))
second = int(input("Input second number:  "))
third = int(input('Input third number: '))
if first == second and first == third:
    print(3)
elif first == second or first == third or second == third:
    print(2)
else:
    print(0)