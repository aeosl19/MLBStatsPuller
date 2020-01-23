import requests

def get_data(url):
    res = requests.get(url)
    try:
        results = res.json()
        return results
    except Exception as ex:
        print (f'Error from get_data with : {ex}')
        return None

