# import os
import urllib.parse

from .rout_map import *


def PhotoFinder(file_url):
    current_directory = os.getcwd()
    directory = os.path.join(current_directory, 'DCIM')

    # Извлекаем имя файла из URL
    parsed_url = urllib.parse.urlparse(file_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    file_path = query_params.get('path', [''])[
        0]  # Получаем путь вида '/12496708/681b48c990fa7b4aae3b4f6b_17466185583977815574159042432153.jpg'

    # Извлекаем имя файла (последняя часть пути)
    file_name = os.path.basename(file_path)  # Получим '681b48c990fa7b4aae3b4f6b_17466185583977815574159042432153.jpg'

    # Если нужно только числовое имя (например, '17466185583977815574159042432153.jpg'), можно разбить по '_'
    file_name = file_name.split('_')[-1]  # Раскомментировать, если нужно только '17466185583977815574159042432153.jpg'

    # Функция для поиска файлов по имени
    def find_file_by_name(directory, file_name):
        for root, dirs, files in os.walk(directory):
            if file_name in files:
                return os.path.join(root, file_name)
        return None

    # Ищем файл
    file_path = find_file_by_name(directory, file_name)

    if not file_path:
        print("Файл не найден.")
        return None
    else:
        print(f"Найден файл: {file_path}")
        return file_path