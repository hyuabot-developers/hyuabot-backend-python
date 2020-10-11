import requests
import os
import lxml
from bs4 import BeautifulSoup


def get_realtime_departure(stop_id, bus_id):
    url = f'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?serviceKey={os.getenv("bus_auth")}&stationId={stop_id}&routeId={bus_id}'
    result = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    arrival_info_list = soup.find('response').find('msgbody')
    if arrival_info_list:
        arrival_info_list = arrival_info_list.find('busarrivalitem')
    else:
        return result

    location, predict_time, remained_seat = arrival_info_list.find('locationno1').text, arrival_info_list.find('predicttime1').text, arrival_info_list.find('remainseatcnt1').text
    result.append({'location': location, 'time': predict_time, 'seat': remained_seat})

    return result


def get_bus_info():
    guest_house_stop = '216000379'
    main_gate_stop = '216000719'
    line_10_1 = '216000068'
    line_3102 = '216000061'
    line_707_1 = '216000070'
    return {"10-1": get_realtime_departure(guest_house_stop, line_10_1), "707-1": get_realtime_departure(main_gate_stop, line_707_1), "3102": get_realtime_departure(guest_house_stop, line_3102)}


print(get_bus_info())