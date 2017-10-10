import requests

'''
import pytz, datetime

tz          = pytz.timezone('Europe/Moscow')
client_time = datetime.datetime.now(tz)
'''


def load_attempts():
    start_page = 1
    api_url = 'http://devman.org/api/challenges/solution_attempts'
    number_of_pages = requests.get(api_url).json()['number_of_pages']
    for page in range(number_of_pages):
        page_url = '{}/?page={}'.format(api_url, int(page + start_page))
        users_data = requests.get(page_url).json()['records']
        for user in users_data:
            yield {
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            }


def get_midnighters():
    pass


if __name__ == '__main__':
    gen= load_attempts()
    for g in gen:
        print(g)
