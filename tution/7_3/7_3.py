import os.path


def custom_write(file_name, strings):
    if os.path.isfile(file_name) is False:
        file = open(file_name, 'x', encoding='utf-8')
        file.close()
    else:
        file = open(file_name, 'a', encoding='utf-8')
        count = 0
        dict1 = {}
        for i in strings:
            j = file.tell()
            file.write(i + '\n')
            count += 1
            dict1.update({(count, j): i})
    return dict1



info = ['Text for tell.', 'Используйте кодировку utf-8.',
    'Because there are 2 languages!', 'Спасибо!']

result = custom_write('test.txt', info)
print(result)

for elem in result.items():
    print(elem)