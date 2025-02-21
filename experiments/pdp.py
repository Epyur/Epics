import os
import requests

# Прямая ссылка на публичный файл на Яндекс.Диске
PUBLIC_FILE_URL = 'https://disk.yandex.ru/i/iXTfLzVahoQ96Q'
if not os.path.exists(os.path.join('.', 'out')):
    # Если директория не существует, создаём её
    os.makedirs(os.path.join('.', 'out'))

else:
    pass
# Новый путь и имя файла для сохранения
NEW_FILE_PATH = 'out/новое_имя_файла.jpg'


# Функция для скачивания публичного файла
def download_public_file(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Файл успешно сохранен по пути: {save_path}")
    else:
        print(f"Ошибка при скачивании файла: {response.text}")


# Запуск функции для скачивания публичного файла
download_public_file(PUBLIC_FILE_URL, NEW_FILE_PATH)