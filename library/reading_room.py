import os
import platform

import requests, requests_cache

import json


def get_reading_room_seat(campus: int, room_id=''):
    if platform.system() != 'Windows':
        requests_cache.install_cache(f'/tmp/reading_room_cache', expire_after=60)
    else:
        requests_cache.install_cache(f'{os.path.dirname(os.path.abspath(__file__))}reading_room_cache', expire_after=60)

    try:
        url = 'https://lib.hanyang.ac.kr/smufu-api/pc/1/rooms-at-seat' if campus else 'https://lib.hanyang.ac.kr/smufu-api/pc/2/rooms-at-seat'
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        return ''

    src = json.loads(res.text)
    total_room = src['data']['list']
    active_room = [x['name'] for x in total_room if x['isActive']]
    if room_id:
        for room in total_room:
            if room['name'] == room_id:
                return room, active_room
    else:
        return total_room, active_room
