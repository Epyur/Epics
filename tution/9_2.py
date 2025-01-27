first_strings = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']

second_strings = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

frst_result = [len(x) for x in first_strings if len(x) > 5]
scnd_result = [(x, y) for x in first_strings for y in second_strings if len(x) == len(y)]
thrd_result = [{x: len(x)} for x in first_strings + second_strings if len(x)%2 == 0]

print(frst_result)
print(*scnd_result)
print(*thrd_result)