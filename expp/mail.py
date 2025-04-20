import requests
import json


# Функция для получения списка задач
def get_issues(queue_name, token):
    # URL API трекера
    url = 'https://api.tracker.yandex.net/v2/issues/'

    # Заголовки запроса
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json'
    }

    # Параметры запроса
    params = {
        'fields': 'id,summary,queue,creator,created,updated',  # Поля для получения
        'query': f'queue:{queue_name}'  # Запрос для получения задач из конкретной очереди
    }

    try:
        # Отправляем GET-запрос
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Проверяем статус ответа

        # Парсим ответ
        issues = response.json()

        # Выводим информацию о задачах
        for issue in issues['issues']:
            print(f"ID: {issue['id']}")
            print(f"Заголовок: {issue['summary']}")
            print(f"Очередь: {issue['queue']['name']}")
            print(f"Создатель: {issue['creator']['display_name']}")
            print(f"Создана: {issue['created']}")
            print(f"Обновлено: {issue['updated']}")
            print("-" * 40)

        return issues

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении задач: {e}")
        return None


# Пример использования
if __name__ == "__main__":
    # Ваш токен доступа
    oauth_token = 'y0__xCaje-jqveAAhiJ9jQgvvf7lhKujjEDXtPwa-QBNLzpPkwk1JgJTw'
    get_issues('LPIZAYAVKINAPRO', oauth_token)