import requests

def my_function():
    session = requests.Session()
    url = "https://api.tracker.yandex.net/v3/issues/_search"
    json = {
        "query": "epic: notEmpty() Queue: LPIZAYAVKINAPRO \"Sort by\": Updated DESC"
    }

    head =  {
        "Authorization": "y0__xCaje-jqveAAhiJ9jQgvvf7lhKujjEDXtPwa-QBNLzpPkwk1JgJTw",
        "X-Org-ID": 'bpfl5bvk5m0vfbrsnumd'
    }
    session.headers.update(head)
    response = session.get(url, params=json)
    try:
        data = response.json()
        print(response)
        print(data)
    except requests.exceptions.JSONDecodeError:
        print("Ошибка декодирования JSON")
        print(response.text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        print(response.text)


my_function()
