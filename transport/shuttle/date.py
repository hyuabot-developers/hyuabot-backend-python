import os
import json
from datetime import datetime

from workalendar.asia import SouthKorea

from common.config import korea_timezone

cal = SouthKorea()


def is_semester(date_to_know=None):
    if not date_to_know:
        date_to_know = datetime.now(tz=korea_timezone)
    # 학기중, 계절학기, 방학 중인지 구별 코드
    # json 파일 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    date_url = f'{current_dir}/timetable/date.json'
    with open(date_url, 'r') as raw_json:
        result = json.load(raw_json)

    for key in [x for x in list(result.keys()) if x not in ['holiday', 'halt']]:
        for term in result[key]:
            start_time = datetime.strptime(term['start'], "%m-%d").replace(tzinfo=korea_timezone)
            end_time = datetime.strptime(term['end'], "%m-%d").replace(tzinfo=korea_timezone)
            if end_time > start_time:
                start_time = start_time.replace(year=date_to_know.year)
                end_time = end_time.replace(year=date_to_know.year)
            else:
                start_time = start_time.replace(year=date_to_know.year)
                end_time = end_time.replace(year=date_to_know.year + 1)
            if start_time <= date_to_know < end_time:
                term_result = key
                break
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

    return term_result, day
