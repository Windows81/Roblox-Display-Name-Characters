from typing import override
import requests
import time
import base
import os

MAX_VALUE = 0xffff


class display_name_database(base.lambda_database):
    INIT_STATEMENTS = ""
    SCHEMA = {
        'CHARACTERS': {
            'iden': {
                'func': lambda iden, data: [iden],
                'type': 'integer primary key',
            },
            'char': {
                'func': lambda iden, data: [chr(iden)],
                'type': 'text',
            },
            'code': {
                'func': lambda iden, data: [data],
                'type': 'text',
            },
        },
    }


class display_name_scraper(base.scraper_base):
    RANGE_MIN: int = 0
    RANGE_MAX: int = MAX_VALUE - 1
    DEFAULT_THREAD_COUNT: int = 3

    @staticmethod
    @override
    def try_entry(iden: int) -> int:
        test_name = chr(iden) * 3
        wait_time = 2
        while True:
            try:
                # Manually replace `1630228` with your user iden number.
                result = requests.get(
                    f'https://users.roblox.com/v1/users/1630228/display-names/validate?displayName={test_name}',
                    cookies={'.ROBLOSECURITY': os.environ['ROBLOSECURITY']},
                ).json()
            except requests.exceptions.ConnectionError:
                continue

            # On success
            if result == {}:
                return -1

            code: int = result["errors"][0]['code']
            if code == 0:  # Too many requests
                time.sleep(wait_time)
                wait_time *= 2**(1/3)
                continue

            return code
