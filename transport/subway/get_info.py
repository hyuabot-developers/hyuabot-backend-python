import os
import requests
import json
import datetime
import time

from common.config import korea_timezone

minute_to_arrival = {
    '한대앞': 0, '중앙': 2, '고잔': 4, '초지': 6.5, '안산': 9, '신길온천': 12.5, '정왕': 16, '오이도': 19, '달월': 21, '월곶': 23,
    '소래포구': 25, '인천논현': 27, '호구포': 29, '상록수': 2, '반월': 6, '대야미': 8.5, '수리산': 11.5, '산본': 13.5, '금정': 18,
    '범계': 21.5, '평촌': 23.5, '인덕원': 26, '정부과천청사': 28, '과천': 30, '사리': 2, '야목': 7, '어천': 10, '오목천': 14,
    '고색': 17, '수원': 21, '매교': 23, '수원시청': 26, '매탄권선': 29}

status_code = {0: '진입', 1: '도착', 2: '출발', 3: '전역출발', 4: '전역진입', 5: '전역도착', 99: '운행중'}


def get_subway_info(campus=0):
    key = os.getenv('metro_auth')
    station = '한양대' if campus else '한대앞'
    url = f'http://swopenapi.seoul.go.kr/api/subway/{key}/json/realtimeStationArrival/0/10/{station}'
    try:
        req = requests.get(url, timeout=3)
    except requests.exceptions.Timeout:
        return None
    arrival_up = []
    arrival_down = []
    if req.status_code == 200:
        if 'realtimeArrivalList' in req.json().keys():
            for arrival_info in req.json()['realtimeArrivalList']:
                updn, end_station, pos, status = arrival_info['updnLine'], arrival_info['bstatnNm'], arrival_info['arvlMsg3'], int(arrival_info['arvlCd'])
                if campus:
                    remained_time = int(arrival_info['barvlDt'])
                elif pos in minute_to_arrival.keys():
                    remained_time = minute_to_arrival[pos]
                else:
                    remained_time = 30.5

                if updn == '상행' or updn == '내선':
                    arrival_up.append({"terminalStn": end_station, "pos": pos, "time": remained_time, "status": status_code[status]})
                else:
                    arrival_down.append({"terminalStn": end_station, "pos": pos, "time": remained_time, "status": status_code[status]})
            return {'up': arrival_up, 'down': arrival_down}
        else:
            return None


def get_subway_timetable(is_weekend=True):
    now = datetime.datetime.now(tz=korea_timezone)
    root_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(root_folder, 'api/subway/suinline.json')
    result = {'up': [], 'down': []}
    with open(json_path, 'r', encoding='utf-8') as f:
        timetable = json.load(f)
    is_weekend = 'weekend' if is_weekend else 'weekdays'

    for key in ['up', 'down']:
        for x in timetable[is_weekend][key]:
            arrival_time = time.strptime(x['time'], "%H:%M:%S")
            arrival_time = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                             hour=arrival_time.tm_hour, minute=arrival_time.tm_min, second=arrival_time.tm_sec,
                                             tzinfo=korea_timezone)
            if arrival_time > now:
                result[key].append({'endStn': x['endStn'], 'time': arrival_time})
    return result
