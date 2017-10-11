from datetime import datetime

import pytz
import requests


def load_attempts():
    start_page = 1
    api_url = 'http://devman.org/api/challenges/solution_attempts'
    number_of_pages = requests.get(api_url).json()['number_of_pages']
    for page in range(number_of_pages):
        page_num = page + start_page
        users_data = requests.get(api_url,
                                  params={'page': page_num}).json()['records']
        for user in users_data:
            yield {
                'username': user['username'],
                'timestamp': user['timestamp'],
                'timezone': user['timezone'],
            }


def check_midnighter(user_info, start_hour=0, stop_hour=5):
    user_timezone = pytz.timezone(user_info['timezone'])
    attempt_time_utc = datetime.utcfromtimestamp(user_info['timestamp'])
    return bool(pytz.utc.localize(attempt_time_utc, is_dst=None).astimezone(
        user_timezone).hour in range(start_hour, stop_hour))


def output_users_to_console(midnigh_users):
    print('This devman users are owls:')
    for midnigh_user in midnigh_users:
        print(midnigh_user)

if __name__ == '__main__':
    generator = load_attempts()
    midnigh_users = set()
    midnigh_users = {user['username'] for user in generator if user[
        'timestamp'] and check_midnighter(user)}
    output_users_to_console(midnigh_users)

