from datetime import datetime

import pytz
import requests


def get_attempt_page(page_num):
    api_url = 'http://devman.org/api/challenges/solution_attempts'
    attempts_page_data = requests.get(api_url, params={'page': page_num})
    return attempts_page_data.json()


def load_attempts():
    start_page = 1
    while True:
        raw_json_data = get_attempt_page(start_page)
        number_of_pages = raw_json_data['number_of_pages']
        attempts_data = raw_json_data['records']
        for attempt in attempts_data:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }
        if start_page < number_of_pages:
            start_page += 1
        else:
            break


def check_midnighter(attempt_info, start_hour=0, stop_hour=5):
    user_timezone = pytz.timezone(attempt_info['timezone'])
    attempt_time_utc = datetime.utcfromtimestamp(attempt_info['timestamp'])
    attempt_hour = pytz.utc.localize(attempt_time_utc, is_dst=None).astimezone(
        user_timezone).hour
    return start_hour <= attempt_hour < stop_hour


def output_users_to_console(midnigh_users_name):
    print('This devman users are owls:')
    for midnigh_user_name in midnigh_users_name:
        print(midnigh_user_name)


if __name__ == '__main__':
    attempts = load_attempts()
    midnigh_users_name = {attempt['username'] for attempt in attempts if
                          attempt['timestamp'] and check_midnighter(attempt)}
    output_users_to_console(midnigh_users_name)
