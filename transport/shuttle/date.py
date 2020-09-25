import requests, requests_cache
from workalendar.asia import SouthKorea

from datetime import datetime
import calendar

cal = SouthKorea()
now = datetime.now()

def is_semester(modified=False, date_to_know=now):

    # 학기중, 계절학기, 방학 중인지 구별 코드
    requests_cache.install_cache('timetable_cache')
    req = requests.get(url="https://raw.githubusercontent.com/jil8885/hanyang-shuttle-timetable/main/date.json")
    result = req.json()

    for key in [x for x in list(result.keys()) if x not in ['holiday', 'halt']]:
        for term in result[key]:
            startTime = datetime.strptime(term['start'], "%m-%d")
            endTime = datetime.strptime(term['end'], "%m-%d")
            if endTime <= startTime:
                startTime = startTime.replace(year=date_to_know.year)
                endTime = endTime.replace(year=date_to_know.year)
            else:
                startTime = startTime.replace(year=date_to_know.year)
                endTime = endTime.replace(year=date_to_know.year + 1)
            
            if date_to_know >= startTime and date_to_know < endTime:
                term = key


    # 운행 중지 일자
    for stop_date in result['halt']:
        halt_date = datetime.strptime(stop_date, "%m-%d")
        if (date_to_know.month, date_to_know.day) == (halt_date.month, halt_date.day):
            term = 'halt'

    # 평일/주말 구분
    if date_to_know.weekday() in [5, 6] or not cal.is_working_day(date_to_know):
        day = 'weekend'
    else:
        day = 'week'

    # 공휴일 구분
    for holiday_date in result['holiday']:
        holiday_date = datetime.strptime(holiday_date, "%m-%d")
        if (date_to_know.month, date_to_know.day) == (holiday_date.month, holiday_date.day):
            day = 'weekend'

    return term, day
