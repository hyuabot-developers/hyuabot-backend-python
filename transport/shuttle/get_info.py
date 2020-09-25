# External Module
import json, os, platform
from datetime import datetime

# Internal Module
from transport.shuttle.date import is_semester # To get which file to use

now = datetime.now(tz='Asia/Seoul')

def get_departure_info(dest_stop):
    # 학기 여부, 주말 여부 연산
    bool_semester, bool_weekend = is_semester()
    
    # 학기 여부에 따라 json 경로 수정
    term = {
        'halt':'/halt',
        'semester':'/semester',
        'vacation_session':'/vacation_session',
        'vacation':'/vacation'
    }

    # 발화 내용에 따라 json 경로 수정
    stop = {
        '기숙사':'Residence',
        '셔틀콕':'Shuttlecock_O',
        '한대앞역':'Subway',
        '예술인A':'Yesulin',
        '셔틀콕 건너편':'Shuttlecock_I',
    }


    # 운행 중지 일자라면 중지한다고 반환
    if term[bool_semester] == '/halt':
        return '오늘 셔틀 운행을 하지 않습니다.'
    else:
        # json 파일 로드
        current_dir = os.path.dirname(os.path.abspath(__file__))

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
            depart_time = depart_time.replace(year=now.year, month=now.month, day=now.day)
            if depart_time >= now:       
                # 순환버스 도착 정보 최대 2개
                if (depart_info['type'] == 'C' or dest_stop == '예술인A') and len(bus_to_come_c) < 2:
                    bus_to_come_c.append(depart_time)
                # 한대앞 직행 버스 도착 정보 최대 2개
                elif (depart_info['type'] == 'DH' or (dest_stop == '한대앞역' and not depart_info['type'])) and len(bus_to_come_dh) < 2:
                    bus_to_come_dh.append(depart_time)
                elif depart_info['type'] == 'DY' and len(bus_to_come_dh) < 2:
                    bus_to_come_dy.append(depart_time)
                elif dest_stop == '셔틀콕 건너편' and depart_info['type'] == 'R':
                    bus_to_come_c.append(depart_time)
                elif (dest_stop == '셔틀콕' or dest_stop == '기숙사') and len(bus_to_come_dh) >= 2 and len(bus_to_come_dy) >= 2 and len(bus_to_come_c) >= 2:
                    break
                elif dest_stop == '한대앞역' and len(bus_to_come_dh) >= 2 and len(bus_to_come_c) >= 2:
                    break
                elif dest_stop == '예술인A' and len(bus_to_come_dy) >= 2 and len(bus_to_come_c) >= 2:
                    break
        return bus_to_come_dh, bus_to_come_dy, bus_to_come_c
                



    