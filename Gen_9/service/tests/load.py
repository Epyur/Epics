import os
import requests
from urllib.parse import unquote, urlparse
from datetime import datetime


def download_yandex_file(file_url, save_folder='downloads'):
    """
    Загружает файл с Яндекс.Форм, обходя ограничения.
    Возвращает путь к файлу или None при ошибке.
    """
    try:
        # Создаем папку для загрузок
        os.makedirs(save_folder, exist_ok=True)

        # Настраиваем сессию с пользовательскими заголовками
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://forms.yandex.ru/'
        }

        # Загружаем файл с проверкой типа содержимого
        response = session.get(file_url, headers=headers, stream=True, timeout=10)

        # Проверяем, что ответ - это изображение
        if 'image/' not in response.headers.get('content-type', ''):
            if '<html' in response.text.lower():
                raise ValueError("Яндекс требует авторизации или ссылка неверна")
            else:
                raise ValueError("Сервер вернул неожиданный тип данных")

        # Извлекаем имя файла
        filename = (
                unquote(urlparse(file_url).path.split('/')[-1])
                or f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        # Сохраняем файл
        save_path = os.path.join(save_folder, filename)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)

        # Проверяем размер файла
        if os.path.getsize(save_path) < 1024:  # Меньше 1KB = вероятно ошибка
            os.remove(save_path)
            raise ValueError("Файл слишком мал (возможно, ошибка загрузки)")

        return save_path

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return None


# Пример использования
file_url = "https://forms.yandex.ru/cloud/files?path=%2F6456219%2F6819d4fae010db8809d11324_17465233724663974015526050807822.jpg"
downloaded_file = download_yandex_file(file_url)

if downloaded_file:
    print(f"Файл сохранен: {downloaded_file}")
else:
    print("Не удалось скачать файл. Попробуйте:")
    print("1. Проверить ссылку вручную в браузере")
    print("2. Авторизоваться в Яндекс.Формах")
    print("3. Использовать VPN, если доступ ограничен")