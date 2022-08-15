import requests

def fetch_tag(name):
    headers = {
        'accept-language': 'en'
    }

    response = requests.get(f'https://www.pixiv.net/ajax/search/tags/{name}', headers=headers)

    if response.status_code != 200:
        return False

    data = response.json()

    if data.get('error', True):
        return False

    return data