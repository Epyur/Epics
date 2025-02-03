import requests

# URL для запроса данных
url = "https://api.wiki.yandex.net/tables/pmipir/lpi/inc/"

# Параметры запроса
headers = {
    "Authorization": f"OAuth {'y0__xCaje-jqveAAhiJ9jQgvvf7lhKujjEDXtPwa-QBNLzpPkwk1JgJTw'}",
    "Content-Type": "application/json"
}

# Параметры для получения данных (например, название страницы)
params = {
    "title": "Заявки"
}

# Выполнение запроса
response = requests.get(url, headers=headers, params=params)

# Проверка статуса ответа
if response.status_code == 200:
    # Извлечение данных из ответа
    data = response.json()
    print(data)
else:
    print(f"Произошла ошибка: {response.status_code}")