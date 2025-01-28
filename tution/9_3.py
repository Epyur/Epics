first = ['Strings', 'Student', 'Computers']

second = ['Строка', 'Урбан', 'Компьютер']

frst_result = (len(x)-len(y) for x, y in zip(first, second) if len(x) != len(y))
scnd_result = (len(first[x]) == len(second[x]) for x in range(len(first)))

print(list(frst_result))
print(list(scnd_result))