# External Module
import json, os, platform
from datetime import datetime

# Internal Module
from transport.shuttle.date import is_semester  # To get which file to use
from common.config import korea_timezone


# 현재 시간 기준 도착 예정 시간
def get_departure_info(dest_stop=None, path=None, num_of_data=None, get_all=False):
    now = datetime.now(tz=korea_timezone)
    # 학기 여부, 주말 여부 연산
    bool_semester, bool_weekend = is_semester()

    if not num_of_data:
        num_of_data = 2

    # 학기 여부에 따라 json 경로 수정
    term = {
        'halt': '/halt',
        'semester': '/semester',
        'vacation_session': '/vacation_session',
        'vacation': '/vacation'
    }

    # 발화 내용에 따라 json 경로 수정
    stop = {
        '기숙사': 'Residence',
        '셔틀콕': 'Shuttlecock_O',
        '한대앞역': 'Subway',
        '예술인A': 'YesulIn',
        '셔틀콕 건너편': 'Shuttlecock_I',
        'Dormitory': 'Residence',
        'Shuttlecock': 'Shuttlecock_O',
        'Station': 'Subway',
        'Terminal': 'YesulIn',
        'Shuttlecock(Oppo)': 'Shuttlecock_I'
    }

    # 운행 중지 일자라면 중지한다고 반환
    if term[bool_semester] == '/halt':
        return '오늘 셔틀 운행을 하지 않습니다.'
    else:
        # json 파일 로드
        current_dir = os.path.dirname(os.path.abspath(__file__))

        if path:
            dest_timetable = f'{current_dir}/timetable{term[bool_semester]}/{bool_weekend}/{path}_{bool_weekend}.json'
        else:
            dest_timetable = f'{current_dir}/timetable{term[bool_semester]}/{bool_weekend}/{stop[dest_stop]}_{bool_weekend}.json'

        # Windows 라면, 경로명 수정
        if platform.system() == 'Windows':
            dest_timetable = dest_timetable.replace('/', '\\')

        with open(dest_timetable, 'r') as raw_json:
            timetable = json.load(raw_json)

        # 표출할 경로
        bus_to_come_c = []
        bus_to_come_dh = []
        bus_to_come_dy = []

        key = list(timetable.keys())[0]
        for depart_info in timetable[key]:
            # 항목별 시간
            depart_time = datetime.strptime(depart_info['time'], '%H:%M')
            depart_time = depart_time.replace(year=now.year, month=now.month, day=now.day, tzinfo=korea_timezone)
            if depart_time >= now and not get_all:
                # 순환버스 도착 정보 최대 2개
                if (depart_info['type'] == 'C' or dest_stop == '예술인A' or dest_stop == 'Terminal' or path == 'YesulIn') and len(bus_to_come_c) < num_of_data:
                    bus_to_come_c.append(depart_time)
                # 한대앞 직행 버스 도착 정보 최대 2개
                elif (depart_info['type'] == 'DH' or ((dest_stop == '한대앞역' or dest_stop == 'Station' or path == 'Subway') and not depart_info['type'])) and len(
                        bus_to_come_dh) < num_of_data:
                    bus_to_come_dh.append(depart_time)
                elif depart_info['type'] == 'DY' and len(bus_to_come_dh) < num_of_data:
                    bus_to_come_dy.append(depart_time)
                elif (dest_stop == '셔틀콕 건너편' or dest_stop == 'Shuttlecock(Oppo)' or path == 'Shuttlecock_I') and depart_info['type'] == 'R' and len(bus_to_come_c) < num_of_data:
                    bus_to_come_c.append(depart_time)
                elif (dest_stop == '셔틀콕' or dest_stop == '기숙사' or dest_stop == 'Shuttlecock' or dest_stop == 'Dormitory' or path == 'Shuttlecock_O' or path == 'Residence') and len(bus_to_come_dh) >= num_of_data and len(
                        bus_to_come_dy) >= num_of_data and len(bus_to_come_c) >= num_of_data:
                    break
                elif (dest_stop == '한대앞역' or dest_stop == 'Station' or path == 'Subway') and len(bus_to_come_dh) >= num_of_data and len(bus_to_come_c) >= num_of_data:
                    break
                elif (dest_stop == '예술인A' or dest_stop == 'Terminal' or path == 'YesulIn') and len(bus_to_come_dy) >= num_of_data and len(bus_to_come_c) >= num_of_data:
                    break
                elif (dest_stop == '셔틀콕 건너편' or dest_stop == 'Shuttlecock(Oppo)' or path == 'Shuttlecock_O') and len(bus_to_come_c) >= num_of_data:
                    break
            elif get_all:
                # 순환버스 도착 정보 최대 2개
                if depart_info['type'] == 'C' or dest_stop == '예술인A' or dest_stop == 'Terminal' or path == 'YesulIn':
                    bus_to_come_c.append(depart_time)
                # 한대앞 직행 버스 도착 정보 최대 2개
                elif depart_info['type'] == 'DH' or ((dest_stop == '한대앞역' or dest_stop == 'Station' or path == 'Subway')
                                                     and not depart_info['type']):
                    bus_to_come_dh.append(depart_time)
                elif depart_info['type'] == 'DY':
                    bus_to_come_dy.append(depart_time)
                elif (dest_stop == '셔틀콕 건너편' or dest_stop == 'Shuttlecock(Oppo)' or path == 'Shuttlecock_I') and \
                        depart_info['type'] == 'R':
                    bus_to_come_c.append(depart_time)
                elif dest_stop == '셔틀콕' or dest_stop == '기숙사' or dest_stop == 'Shuttlecock' or dest_stop == 'Dormitory'\
                        or path == 'Shuttlecock_O' or path == 'Residence':
                    break
                elif dest_stop == '한대앞역' or dest_stop == 'Station' or path == 'Subway':
                    break
                elif dest_stop == '예술인A' or dest_stop == 'Terminal' or path == 'YesulIn':
                    break
                elif dest_stop == '셔틀콕 건너편' or dest_stop == 'Shuttlecock(Oppo)' or path == 'Shuttlecock_O':
                    break
        return bus_to_come_dh, bus_to_come_dy, bus_to_come_c, now


# 첫막차 계산
def get_first_last_departure(dest_stop=None, path=None):
    # 학기 여부, 주말 여부 연산
    bool_semester, bool_weekend = is_semester()
    now = datetime.now(tz=korea_timezone)

    # 학기 여부에 따라 json 경로 수정
    term = {
        'halt': '/halt',
        'semester': '/semester',
        'vacation_session': '/vacation_session',
        'vacation': '/vacation'
    }

    if not path:
        # 발화 내용에 따라 json 경로 수정
        stop = {
            '기숙사': 'Residence',
            '셔틀콕': 'Shuttlecock_O',
            '한대앞역': 'Subway',
            '예술인A': 'YesulIn',
            '셔틀콕 건너편': 'Shuttlecock_I',
            'Dormitory': 'Residence',
            'Shuttlecock': 'Shuttlecock_O',
            'Station': 'Subway',
            'Terminal': 'YesulIn',
            'Shuttlecock(Oppo)': 'Shuttlecock_I',
        }
        path = stop[dest_stop]

    # 운행 중지 일자라면 중지한다고 반환
    if bool_semester == 'halt':
        return bool_semester, bool_weekend, [], [], []
    else:
        # json 파일 로드
        current_dir = os.path.dirname(os.path.abspath(__file__))

        dest_timetable = f'{current_dir}/timetable{term[bool_semester]}/{bool_weekend}/{path}_{bool_weekend}.json'

        # Windows 라면, 경로명 수정
        if platform.system() == 'Windows':
            dest_timetable = dest_timetable.replace('/', '\\')

        with open(dest_timetable, 'r') as raw_json:
            timetable = json.load(raw_json)

        # 표출할 경로
        bus_to_come_c = []
        bus_to_come_dh = []
        bus_to_come_dy = []

        key = list(timetable.keys())[0]
        for depart_info in timetable[key]:
            # 항목별 시간
            depart_time = datetime.strptime(depart_info['time'], '%H:%M')
            depart_time = depart_time.replace(year=now.year, month=now.month, day=now.day, tzinfo=korea_timezone)
            # 순환버스 도착 정보 최대 2개
            if depart_info['type'] == 'C' or dest_stop == '예술인A':
                bus_to_come_c.append(depart_time)
            # 한대앞 직행 버스 도착 정보 최대 2개
            elif depart_info['type'] == 'DH' or (dest_stop == '한대앞역' and not depart_info['type']):
                bus_to_come_dh.append(depart_time)
            elif depart_info['type'] == 'DY':
                bus_to_come_dy.append(depart_time)
            elif dest_stop == '셔틀콕 건너편':
                if depart_info['type'] == 'C':
                    bus_to_come_c.append(depart_time)
                elif depart_info['type'] == "DH":
                    bus_to_come_dh.append(depart_time)
                elif depart_info['type'] == "DY":
                    bus_to_come_dy.append(depart_time)

            if bus_to_come_dh:
                bus_to_come_dh = [bus_to_come_dh[0], bus_to_come_dh[-1]]
            if bus_to_come_dy:
                bus_to_come_dy = [bus_to_come_dy[0], bus_to_come_dy[-1]]
            if bus_to_come_c:
                bus_to_come_c = [bus_to_come_c[0], bus_to_come_c[-1]]

        return bool_semester, bool_weekend, bus_to_come_dh, bus_to_come_dy, bus_to_come_c
