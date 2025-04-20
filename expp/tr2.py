import requests
import json
from oauth2client.client import OAuth2WebServerFlow

class TrackerAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.tracker.yandex.net/v3'
        self.headers = {
            'Authorization': f'OAuth {self.token}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f'{self.base_url}/{endpoint}'
        response = requests.request(
            method,
            url,
            headers=self.headers,
            params=params,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_projects(self):
        return self._make_request('GET', 'projects')

    def get_issues(self, queue=None):
        params = {}
        if queue:
            params['$filter'] = f'queue = "{queue}"'
        return self._make_request('GET', 'issues', params=params)

    def create_issue(self, data):
        return self._make_request('POST', 'issues', data=data)

    def update_issue(self, issue_id, data):
        return self._make_request('PATCH', f'issues/{issue_id}', data=data)

    def get_comments(self, issue_id):
        return self._make_request('GET', f'issues/{issue_id}/comments')


# Настройки для OAuth
CLIENT_ID = 'bf6f1aa287464b6e95d8d97b37e6f9f8'
CLIENT_SECRET = '8d6da104524a44989eff31d61b2b97cc'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'  # Для локальной разработки
SCOPE = 'https://api.tracker.yandex.net/oauth/scope'


def get_oauth_token():
    flow = OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    # Получаем URL для авторизации
    auth_url = flow.step1_get_authorize_url()
    print(f"Перейдите по ссылке для авторизации: {auth_url}")

    # Вводим полученный код
    code = input('Введите код авторизации: ')

    # Получаем токен
    credentials = flow.step2_exchange(code)
    return credentials.access_token

# Получаем токен
token = get_oauth_token()

# Создаем экземпляр API
tracker = TrackerAPI(token)

# Получение проектов
projects = tracker.get_projects()
print(json.dumps(projects, ensure_ascii=False, indent=2))

# Получение задач определенного проекта
issues = tracker.get_issues('LPIZAYAVKINAPRO')
print(json.dumps(issues, ensure_ascii=False, indent=2))

# Создание новой задачи
new_issue = {
    "summary": "Новая задача",
    "description": "Описание задачи",
    "queue": "QUEUE_ID",
    "creator": "USER_ID"
}
created_issue = tracker.create_issue(new_issue)
print(json.dumps(created_issue, ensure_ascii=False, indent=2))

# Обновление задачи
update_data = {
    "summary": "Обновленное название",
    "status": "IN_PROGRESS"
}
updated_issue = tracker.update_issue('ISSUE_ID', update_data)
print(json.dumps(updated_issue, ensure_ascii=False, indent=2))

# Получение комментариев
comments = tracker.get_comments('ISSUE_ID')
print(json.dumps(comments, ensure_ascii=False, indent=2))
