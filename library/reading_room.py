import requests, requests_cache

import json

def get_reading_room_seat(campus:int, room_id=0):

    requests_cache.install_cache('readingroom_cache')
    try:
        url = 'https://lib.hanyang.ac.kr/smufu-api/pc/1/rooms-at-seat' if campus else 'https://lib.hanyang.ac.kr/smufu-api/pc/2/rooms-at-seat'
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        return ''

    src = json.loads(res.text)
    total_room = src['data']['list']
    
    result_str = ''
    active_room = []
    if room_id:
        pass
    else:
        for reading_room in total_room:
            name, is_active, total, active, occupied, available = reading_room['name'], reading_room['isActive'], reading_room['total'], reading_room['activeTotal'], reading_room['occupied'], reading_room['available']
            if is_active:
                active_room.append(name)
                result_str += f"{name} {available}/{active}\n"
    return result_str.strip(), active_room
