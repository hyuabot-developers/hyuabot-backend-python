import datetime
import json
import os
import psycopg2

from copy import deepcopy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .food.food_main import make_string_food, make_string_food2
from .library.lib_main import crawling_lib, crawling_lib2
from .transport.shuttle_main import shuttle_main
from .transport.shuttle.date import is_seasonal, is_semester


# global variables
host = os.getenv("dbhost")
name = os.getenv("dbname")
dbuser = os.getenv("dbuser")
password = os.getenv("dbpassword")
connection = f"host='{host}' dbname={name} user='{dbuser}' password='{password}'"

# global answer
base_response = {'version': '2.0', 'template': {'outputs': [], 'quickReplies': []}}


# Get users answer and user key.
def json_parser(request):
    answer = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    user = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']
    return answer, user


# Get User info.
def get_user(user_key):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    sql = 'select * from userinfo where id=%s'
    cursor.execute('create table if not exists userinfo(id text, campus text)')
    cursor.execute(sql, (user_key,))
    user_info = cursor.fetchall()
    cursor.close()
    conn.close()
    return user_info


# Insert User Info
def create_user(user_key, campus):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    sql = 'INSERT INTO userinfo(id, campus) values (%s, %s)'
    cursor.execute('create table if not exists userinfo(id text, campus text)')
    cursor.execute(sql, (user_key, campus))
    cursor.close()
    conn.close()


# Update User Info
def update_user(user_key, campus):
    conn = psycopg2.connect(connection)
    cursor = conn.cursor()
    sql = f'update userinfo set campus={campus} where id=%s'
    cursor.execute(sql, user_key)
    cursor.close()
    conn.close()


# Make Image Answer
def insert_image(image_url, alt_text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleImage": {"imageUrl": image_url, "altText": alt_text}}]
    return new_response


# Make Text Answer
def insert_text(text):
    new_response = deepcopy(base_response)
    new_response['template']['outputs'] = [{"simpleText": {"text": text}}]
    return new_response


# Insert Quick Replies
def insert_replies(new_response, reply):
    new_response['template']['quickReplies'].append(reply)
    return new_response


# Make Reply
def make_reply(label, message, block_id):
    return {'action': 'block', 'label': label, 'messageText': message, 'blockId': block_id}


# Get CampusInfo
def is_seoul(user_list):
    return user_list[0][1]


@csrf_exempt
def shuttle_photo(request):
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    base_link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/"
    if is_semester(now.month, now.day):
        path = "semester.jpg"
        string = "학기중입니다."
    elif is_seasonal(now.month, now.day):
        path = "seasonal.jpg"
        string = "계절학기 입니다."
    else:
        path = "vacation.jpg"
        string = "방학중입니다."
    response = insert_image(base_link + path, string)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def shuttle(request):
    answer, user = json_parser(request)
    stop_list = {"셔틀콕": "shuttle", "한대앞역": "station", "예술인A": "terminal", "기숙사": "dormitory"}
    if "도착정보입니다" in answer:
        stop = stop_list[answer.split("의")[0]]
    else:
        stop = stop_list[answer.split(" ")[1]]
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    rest_date = [(12, 25), (1, 1)]
    if (now.month, now.day) in rest_date:
        string = "당일, %d월 %d일은 셔틀 미운행합니다." % (now.month, now.day)
    else:
        if is_semester(now.month, now.day):
            string = "학기중 시간표입니다.\n"
        elif is_seasonal(now.month, now.day):
            string = "계절학기 시간표입니다.\n"
        else:
            string = "방학중 시간표입니다.\n"
        # 셔틀콕 도착 정보
        if stop == "shuttle":
            string += '셔틀콕 → 한대앞\n'
            string += shuttle_main('shuttleA', 'toSubway') + '\n\n'
            string += '셔틀콕 → 예술인A\n'
            string += shuttle_main('shuttleB', 'toTerminal') + '\n\n'
            string += '셔틀콕 → 한대앞 → 예술인A\n'
            string += shuttle_main('shuttleA', 'cycle') + '\n\n'
            string += '셔틀콕 건너편 → 기숙사\n'
            string += shuttle_main('shuttleC')
        # 한대앞역 도착 정보
        elif stop == "station":
            string += shuttle_main('subway')
        # 예술인A 도착 정보
        elif stop == "terminal":
            string += shuttle_main('terminal')
        # 창의인재원 도착 정보
        elif stop == "dormitory":
            string += shuttle_main('dorm')
    block_id = '5cc3dc8ee82127558b7e6eba'
    response = insert_text(string)
    for stop in stop_list.keys():
        message = f"{stop}의 셔틀버스 도착 정보입니다"
        reply = make_reply(stop, message, block_id)
        response = insert_replies(response, reply)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def food(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5eaa9b11cdbc3a00015a23fb'
    seoul_restaurant = ['학생식당', '신학생식당', '교직원식당', '신교직원식당', '제1생활관식당', '제2생활관식당', '사랑방', '행원파크']
    erica_restaurant = ['학생식당', '교직원식당', '창의인재원식당', '창업보육센터', '푸드코트']
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 전환되었습니다.')
            for restaurant in seoul_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 전환되었습니다.')
            for restaurant in erica_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        else:
            block_id = '5cc3effc384c5508fceec584'
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif "의 식단입니다" in answer:
        store = answer.split("의 식단")[0]
        if not is_seoul(user_info):
            string = make_string_food(store)
            response = insert_text(string)
            for restaurant in erica_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
        else:
            string = make_string_food2(store)
            response = insert_text(string)
            for restaurant in seoul_restaurant:
                reply = make_reply(restaurant, f"{restaurant}의 식단입니다", block_id)
                response = insert_replies(response, reply)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def library(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5e0df82cffa74800014bc838'
    seoul_lib = ['제1열람실', '제2열람실', '제3열람실', '제4열람실', '법학 대학원열람실', '법학 제1열람실', '법학 제2열람실A', '법학 제2열람실B']
    erica_lib = ['제1열람실', '제3열람실', '제4열람실', '제5열람실']
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 지정되었습니다.')
            for lib in seoul_lib:
                reply = make_reply(lib, f"{lib}의 좌석정보입니다.", block_id)
                response = insert_replies(response, reply)
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 지정되었습니다.')
            for lib in erica_lib:
                reply = make_reply(lib, f"{lib}의 좌석정보입니다.", block_id)
                response = insert_replies(response, reply)
        else:
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif is_seoul(user_info):
        if "열람실 정보" in answer:
            location = 0
        elif "법학" in answer:
            if "대학원" in answer:
                location = 1
            elif "제1" in answer:
                location = 2
            elif "A" in answer:
                location = 3
            elif "B" in answer:
                location = 4
        else:
            if "제1" in answer:
                location = 5
            elif "제2" in answer:
                location = 6
            elif "제3" in answer:
                location = 7
            elif "제4" in answer:
                location = 8
        string = crawling_lib2(int(location))
        response = insert_text(string)
        for lib in seoul_lib:
            reply = make_reply(lib, f"{lib}의 좌석정보입니다.", block_id)
            response = insert_replies(response, reply)
    else:
        if "열람실 정보" in answer:
            location = 0
        elif "좌석정보입니다." in answer:
            location = answer[1]
        string = crawling_lib(int(location))
        response = insert_text(string)
        for lib in erica_lib:
            reply = make_reply(lib, f"{lib}의 좌석정보입니다.", block_id)
            response = insert_replies(response, reply)
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def update_campus(request):
    answer, user = json_parser(request)
    user_info = get_user(user)
    block_id = '5eaa9bf741559f000197775d'
    if not user_info:
        if '서울' in answer:
            create_user(user, 1)
            response = insert_text('서울캠퍼스로 전환되었습니다.')
        elif 'ERICA' in answer:
            create_user(user, 0)
            response = insert_text('ERICA 캠퍼스로 전환되었습니다.')

        else:
            campuses = ['서울', 'ERICA']
            response = insert_text('캠퍼스를 지정해주십시오')
            for campus in campuses:
                reply = make_reply(campus, f"{campus}로 지정되었습니다.", block_id)
                response = insert_replies(response, reply)
    elif not is_seoul(user_info):
        update_user(get_user(user_info), 1)
        response = insert_text('서울캠퍼스로 전환되었습니다.')
    else:
        update_user(get_user(user_info), 0)
        response = insert_text('ERICA 캠퍼스로 전환되었습니다.')
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
