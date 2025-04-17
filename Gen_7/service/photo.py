# import os
from .rout_map import *

def PhotoFinder(file_num):
    current_directory = os.getcwd()
    directory = os.path.join(current_directory, 'DCIM')

    # Укажите часть имени файла, которую нужно найти
    search_part = str(file_num)  # Замените на нужную часть имени файла


    # Функция для поиска файлов по части имени и возврата полного пути
    def find_files_by_name_part(directory, search_part):
        found_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if search_part in file:
                    found_files.append(os.path.join(root, file))
        return found_files

    # Пример использования
    file_paths = find_files_by_name_part(directory, search_part)

    # Вывод полного пути к найденным файлам
    if not file_paths:
        pass
        # print("Файлы не найдены.")
    else:
        path = file_paths[0]
        # print(path)
    return path