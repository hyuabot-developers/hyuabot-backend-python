import requests
import os
import lxml
from bs4 import BeautifulSoup
import datetime
import json
import time

from common.config import korea_timezone


def get_realtime_departure(stop_id, bus_id):
    url = f'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={os.getenv("bus_auth")}&stationId={stop_id}&routeId={bus_id}'
    result = []
    try:
        req = requests.get(url, timeout=2)
        soup = BeautifulSoup(req.text, 'lxml')
        arrival_info_list = soup.find('response').find('msgbody')
        if arrival_info_list:
            arrival_info_list = arrival_info_list.find('busarrivalitem')
        else:
            return result

        location, predict_time, remained_seat = arrival_info_list.find('locationno1').text, arrival_info_list.find('predicttime1').text, arrival_info_list.find('remainseatcnt1').text
        result.append({'location': location, 'time': predict_time, 'seat': remained_seat})

        return result
    except AttributeError:
        return []
    except requests.exceptions.Timeout:
        return []


def get_bus_info():
    guest_house_stop = '216000379'
    main_gate_stop = '216000719'
    line_10_1 = '216000068'
    line_3102 = '216000061'
    line_707_1 = '216000070'
    return {"10-1": get_realtime_departure(guest_house_stop, line_10_1), "707-1": get_realtime_departure(main_gate_stop, line_707_1), "3102": get_realtime_departure(guest_house_stop, line_3102)}


def get_bus_timetable(weekdays=0, routeNum=None):
    now = datetime.datetime.now(tz=korea_timezone)
    root_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(root_folder, 'api/bus/timetable.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        timetable = json.load(f)

    if weekdays == 5:
        key = 'sat'
    elif weekdays == 6:
        key = 'sun'
    else:
        key = 'weekdays'

    if routeNum:
        result = []
        for x in timetable[routeNum][key]:
            arrival_time = time.strptime(x['time'], "%H:%M")
            arrival_time = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                             hour=arrival_time.tm_hour, minute=arrival_time.tm_min,
                                             tzinfo=korea_timezone)
            if arrival_time > now:
                result.append({'time': arrival_time})
    else:
        result = {'10-1': [], '3102': [], '707-1': []}
        for route in ['10-1', '3102']:
            for x in timetable[route][key]:
                arrival_time = time.strptime(x['time'], "%H:%M")
                arrival_time = datetime.datetime(year=now.year, month=now.month, day=now.day,
                                                 hour=arrival_time.tm_hour, minute=arrival_time.tm_min, tzinfo=korea_timezone)
                if arrival_time > now:
                    result[route].append({'time': arrival_time})
    return result