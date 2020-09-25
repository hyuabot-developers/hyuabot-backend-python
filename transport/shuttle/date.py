import requests, requests_cache
from datetime import datetime
import calendar

def is_semester(modified=False):
    now = datetime.now()

    # 학기중, 계절학기, 방학 중인지 구별 코드
    requests_cache.install_cache('timetable_cache')
    req = requests.get(url="https://raw.githubusercontent.com/jil8885/hanyang-shuttle-timetable/main/date.json")
    result = req.json()
    for stop_date in result['halt']:
        halt_date = datetime.strptime(term['start'], "%m-%d")
        if (now.month, now.day) == (halt_date.month, halt_date.day):
            return 'halt'
    for key in list(result.keys()).remove('halt'):
        for term in result[key]:
            startTime = datetime.strptime(term['start'], "%m-%d")
            endTime = datetime.strptime(term['end'], "%m-%d")
            if endTime <= startTime:
                startTime = startTime.replace(year=now.year)
                endTime = endTime.replace(year=now.year)
            else:
                startTime = startTime.replace(year=now.year)
                endTime = endTime.replace(year=now.year + 1)

            if startTime.day > calendar.monthrange(startTime.year, startTime.month)[1]:
                startTime = startTime.replace(day=calendar.monthrange(startTime.year, startTime.month)[1])

            if endTime.day > calendar.monthrange(endTime.year, endTime.month)[1]:
                endTime = endTime.replace(day=calendar.monthrange(endTime.year, endTime.month)[1])

            endTime = endTime.replace(hour=23, minute=59, second=59)
            
            if now >= startTime and now <= endTime:
                return key
