from . import shuttle
import datetime
try:
    from .date import is_semester, is_seasonal
except:
    from date import is_semester, is_seasonal

def make_string(where, destination):
    received_json = shuttle.request()
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    timetable = received_json[where]
    arrival_list = []
    string = ""
    busstoplist = ['shuttleA', 'shuttleB', 'shuttleC', 'subway', 'terminal', 'dorm']
    if where == "shuttleA" or where == "shuttleB":
        type_list = {'cycle': '순환버스', 'toSubway': '한대앞행', 'toTerminal': '예술인행'}
    elif where == "shuttleC":
        type_list = {'cycle': '기숙사행', 'toSubway': '기숙사행', 'toTerminal': '기숙사행', "null" : "셔틀콕 종착"}
    else:
        type_list = {'cycle': '순환버스', 'toSubway': '셔틀콕행', 'toTerminal': '셔틀콕행'}
    pos = 0
    if destination is not None:
        for x in timetable:
            if x['type'] == destination and (int(x['time'].split(':')[0]) > now.hour or (int(x['time'].split(':')[0]) == now.hour and int(x['time'].split(':')[1]) > now.minute)):
                arrival_list.append(x)
    else:
        for x in timetable:
            if int(x['time'].split(':')[0]) > now.hour or (int(x['time'].split(':')[0]) == now.hour and int(x['time'].split(':')[1]) > now.minute):
                arrival_list.append(x)
    for x in arrival_list:
        if pos < 2:
            string += type_list[x['type']] + ' ' + x['time'] + ' 도착예정\n'
            pos += 1
    if string == '':
        string += '도착 예정인 버스가 없습니다.'
    if string[-1] == '\n':
        string = string[:-1]
    return string



def make2_string(route):
    received_json = shuttle.request2()
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    come_list = ["route1", "route2", "route3", "route4", "route5"]
    go_list = ["routeA", "routeB", "routeC", "routeD"]
    info = received_json[route]
    string = ""
    if route in come_list:
        for x in range(len(info)):
            string += info[x]['time'] +"/"
            string += info[x]['stop'] + '\n'
            stop_hour = int(info[x]['time'].split(':')[0])
            stop_min = int(info[x]['time'].split(':')[1])
            arrival = False
            if stop_hour < now.hour or (stop_hour == now.hour and stop_min < now.minute):
                laststop = x
            if laststop == len(info) - 1:
                arrival = True
        if x == len(info) - 1 and arrival:
            string += "현재 예상 위치: 학교 도착"
        else:
            string += "현재 예상 위치:" + info[laststop]['stop'] +"~" + info[laststop + 1]['stop']
    else:
        for x in info:
            string += x['stop'] + '\n'
        string += "하교 버스 출발 시간은 17시 40분입니다."
    return string