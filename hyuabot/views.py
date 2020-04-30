from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import files from subdirectories (하위폴더에서 파일 임포트)
# from .transport.subway import subway_erica
# from .transport.bus import bus_request
from .transport.shuttle_main import shuttle_main, schoolbus_main
from .food.food_main import make_string_food, make_string_food2
from .library.lib_main import crawling_lib, crawling_lib2
from .phone.phone_search import phonesearch
# from .food.food_main import make_string_food
import datetime, json
import requests
import os, psycopg2

# Create your views here.
def home(request):
    return render(request, "home.html")


# from kakaotalkbot setting they post json file to /api/shuttle/busstop to get shuttle info for specific bus stop
# 특정 정류장에 대한 셔틀 도착 정보를 /api/shuttle/정류장(ex. /api/bus/shuttle 으로 셔틀콕 셔틀 도착 정보를 요청받음)
# 오늘이 학기 중인지, 주말인지 구별하는 코드
# 오늘이 학기 중인지, 주말인지 구별하는 코드
def is_semester(month, day):
    semester = [4, 5, 9, 10, 11]
    vacation = [1, 2, 7, 8]
    return False  
    # if month in semester:
    #     return True
    # elif month in vacation:
    #     return False
    # elif month == 3:
    #     if day < 28:
    #         return False
    #     else:
    #         return True
    # else:
    #     if day < 22:
    #         return True
    #     else:
    #         return False

def is_seasonal(month, day):
    # 2020 plan
    if ((month == 6 and day > 21) or (month == 7 and day < 11)) or ((month == 12 and day > 23) or (month == 1 and day < 16)):
        return True
    else:
        return False
@csrf_exempt
def shuttlephoto(request):
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    if is_semester(now.month, now.day):
        link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/semester.jpg"
        string = "학기중입니다."
    elif is_seasonal(now.month, now.day):
        link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/seasonal.jpg"
        string = "계절학기 입니다."
    else:
        link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/vacation.jpg"
        string = "방학중입니다."
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleImage":
                     {"imageUrl": link, "altText": string}
                 }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
    
@csrf_exempt
def shuttle(request):
    response = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    busstop_list = {"셔틀콕":"shuttle","한대앞역":"station","예술인A":"terminal","기숙사":"dormitory"}
    if "도착정보입니다" in response:
        busstop = busstop_list[response.split("의")[0]]
    else:
        busstop = busstop_list[response.split(" ")[1]]
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    rest_date = [(12,25), (1,1)]
    if (now.month, now.day) in rest_date:
        string = "당일, %d월 %d일은 셔틀 미운행합니다."%(now.month, now.day)
    else:
        if is_semester(now.month, now.day):
            string = "학기중 시간표입니다.\n"
        elif is_seasonal(now.month, now.day):
            string = "계절학기 시간표입니다.\n"
        else:
            string ="방학중 시간표입니다.\n"
        # 셔틀콕 도착 정보
        if busstop == "shuttle":
            string += '셔틀콕 → 한대앞\n'
            string += shuttle_main('shuttleA', 'toSubway') + '\n\n'
            string += '셔틀콕 → 예술인A\n'
            string += shuttle_main('shuttleB', 'toTerminal') + '\n\n'
            string += '셔틀콕 → 한대앞 → 예술인A\n'
            string += shuttle_main('shuttleA', 'cycle') + '\n\n'
            string += '셔틀콕 건너편 → 기숙사\n'
            string += shuttle_main('shuttleC')
        # 한대앞역 도착 정보
        elif busstop == "station":
            string += shuttle_main('subway')
        # 예술인A 도착 정보
        elif busstop == "terminal":
            string += shuttle_main('terminal')
        # 창의인재원 도착 정보
        elif busstop == "dormitory":
            string += shuttle_main('dorm')
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText":
                     {"text": string}
                 }
            ],
            "quickReplies":[
                {
                    "action" : "block",
                    "label" : "🏫 셔틀콕",
                    "messageText" : "셔틀콕의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc8ee82127558b7e6eba"
                },
                {
                    "action" : "block",
                    "label" : "🚆 한대앞역",
                    "messageText" : "한대앞역의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc97e82127558b7e6ebc"
                },
                {
                    "action" : "block",
                    "label" : "🚍 예술인A",
                    "messageText" : "예술인A의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc9f5f38dd4c34bad81b"
                },
                {
                    "action" : "block",
                    "label" : "🏘️ 기숙사",
                    "messageText" : "기숙사의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc865f38dd4c34bad819"
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def food(request):
    conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
    conn = psycopg2.connect(conn_sql)
    cursor = conn.cursor()
    string = ""
    store = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    user = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']
    sql = "select * from userinfo where id=%s"
    cursor.execute('create table if not exists userinfo(id text, campus text)')
    cursor.execute(sql, (user,))
    userinfo = cursor.fetchall()
    if userinfo == []:
        if store in ["서울", "ERICA"]:
            sql = "INSERT INTO userinfo(id, campus) values (%s, %s)"
            if store == "서울":
                cursor.execute(sql, (id, 1))
                conn.commit()
                responseBody = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {"simpleText":
                                {"text": '서울캠퍼스로 전환되었습니다.'}
                            }
                        ],
                        "quickReplies":[
                            {
                                "action" : "block",
                                "label" : "교직원식당",
                                "messageText" : "교직원식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "학생식당",
                                "messageText" : "학생식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "사랑방",
                                "messageText" : "사랑방의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "행원파크",
                                "messageText" : "행원파크의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "신교직원식당",
                                "messageText" : "신교직원식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "신학생식당",
                                "messageText" : "신학생식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "제1생활관식당",
                                "messageText" : "제1생활관의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "제2생활관식당",
                                "messageText" : "제2생활관식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                        ]
                    }
                }
                return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
            else:
                cursor.execute(sql, (id, 0))
                conn.commit()
                responseBody = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {"simpleText":
                                {"text": 'ERICA 캠퍼스로 전환되었습니다.'}
                            }
                        ],
                        "quickReplies":[
                            {
                                "action" : "block",
                                "label" : "학생식당",
                                "messageText" : "학생식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "교직원식당",
                                "messageText" : "교직원식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "창업보육센터",
                                "messageText" : "창업보육센터의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "푸드코트",
                                "messageText" : "푸드코트의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            },
                            {
                                "action" : "block",
                                "label" : "창의인재원식당",
                                "messageText" : "창의인재원식당의 식단입니다.",
                                "blockId" : "5eaa9b11cdbc3a00015a23fb"
                            }
                        ]
                    }
                }
            return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
        else:
            responseBody = {"version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": '캠퍼스를 지정해주십시오'}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "🏫 서울",
                        "messageText" : "서울캠퍼스로 전환되었습니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "🏫 ERICA",
                        "messageText" : "ERICA 캠퍼스로 전환되었습니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    }
                ]
            }
        }
        return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
    if "의 식단입니다" in store:
        store = store.split("의 식단")[0]
    if userinfo[0][1] == '0':
        string = make_string_food(store)
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": string}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "학생식당",
                        "messageText" : "학생식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "교직원식당",
                        "messageText" : "교직원식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "창업보육센터",
                        "messageText" : "창업보육센터의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "푸드코트",
                        "messageText" : "푸드코트의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "창의인재원식당",
                        "messageText" : "창의인재원식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    }
                ]
            }
        }
    elif userinfo[0][1] == '1':
        string = make_string_food2(store)
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": string}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "교직원식당",
                        "messageText" : "교직원식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "학생식당",
                        "messageText" : "학생식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "사랑방",
                        "messageText" : "사랑방의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "행원파크",
                        "messageText" : "행원파크의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "신교직원식당",
                        "messageText" : "신교직원식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "신학생식당",
                        "messageText" : "신학생식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "제1생활관식당",
                        "messageText" : "제1생활관의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                    {
                        "action" : "block",
                        "label" : "제2생활관식당",
                        "messageText" : "제2생활관식당의 식단입니다.",
                        "blockId" : "5eaa9b11cdbc3a00015a23fb"
                    },
                ]
            }
        }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def library(request):
    conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
    conn = psycopg2.connect(conn_sql)
    cursor = conn.cursor()
    string = ""
    location = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    user = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']
    sql = "select * from userinfo where id=%s"
    cursor.execute('create table if not exists userinfo(id text, campus text)')
    cursor.execute(sql,(user,))
    conn.commit()
    userinfo = cursor.fetchall()
    if userinfo == []:
        if "서울" in location or "ERICA" in location:
            sql = "INSERT INTO userinfo(id, campus) values (%s, %s)"
            if "서울" in location:
                cursor.execute(sql, (id, 1))
                responseBody = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {"simpleText":
                                {"text": '서울캠퍼스로 전환되었습니다.'}
                            }
                        ],
                        "quickReplies":[
                            {
                                "action" : "block",
                                "label" : "📖 제1열람실",
                                "messageText" : "제1열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제2열람실",
                                "messageText" : "제2열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제3열람실",
                                "messageText" : "제3열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제4열람실",
                                "messageText" : "제4열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 법학 대학원열람실",
                                "messageText" : "법학 대학원열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 법학 제1열람실",
                                "messageText" : "법학 제1열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 법학 제2열람실A",
                                "messageText" : "법학 제2열람실A의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 법학 제2열람실B",
                                "messageText" : "법학 제2열람실B의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                        ]
                    }
                }
            else:
                cursor.execute(sql, (id, 0))
                conn.commit()
                responseBody = {
                    "version": "2.0",
                    "template": {
                        "outputs": [
                            {"simpleText":
                                {"text": string}
                            }
                        ],
                        "quickReplies":[
                            {
                                "action" : "block",
                                "label" : "📖 제1열람실",
                                "messageText" : "제1열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제3열람실",
                                "messageText" : "제3열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제4열람실",
                                "messageText" : "제4열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            },
                            {
                                "action" : "block",
                                "label" : "📖 제5열람실",
                                "messageText" : "제5열람실의 좌석정보입니다.",
                                "blockId" : "5e0df82cffa74800014bc838"
                            }
                        ]
                    }
                }
        else:
            responseBody = {"version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": '캠퍼스를 지정해주십시오'}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "🏫 서울",
                        "messageText" : "서울캠퍼스로 전환되었습니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "🏫 ERICA",
                        "messageText" : "ERICA 캠퍼스로 전환되었습니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    }
                ]
            }
        }
        return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
    elif userinfo[0][1] == '0':
        if "열람실 정보" in location:
            location = 0
        elif "좌석정보입니다." in location:
            location = location[1]
        string = crawling_lib(int(location))
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": string}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "📖 제1열람실",
                        "messageText" : "제1열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제3열람실",
                        "messageText" : "제3열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제4열람실",
                        "messageText" : "제4열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제5열람실",
                        "messageText" : "제5열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    }
                ]
            }
        }
    elif userinfo[0][1] == '1':
        if "열람실 정보" in location:
            location = 0
        elif "법학" in location:
            if "대학원" in location:
                location = 1
            elif "제1" in location:
                location = 2
            elif "A" in location:
                location = 3
            elif "B" in location:
                location = 4
        else:
            if "제1" in location:
                location = 5
            elif "제2" in location:
                location = 6
            elif "제3" in location:
                location = 7
            elif "제4" in location:
                location = 8
        string = crawling_lib2(int(location))
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": string}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "📖 제1열람실",
                        "messageText" : "제1열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제2열람실",
                        "messageText" : "제2열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제3열람실",
                        "messageText" : "제3열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 제4열람실",
                        "messageText" : "제4열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 법학 대학원열람실",
                        "messageText" : "법학 대학원열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 법학 제1열람실",
                        "messageText" : "법학 제1열람실의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 법학 제2열람실A",
                        "messageText" : "법학 제2열람실A의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                    {
                        "action" : "block",
                        "label" : "📖 법학 제2열람실B",
                        "messageText" : "법학 제2열람실B의 좌석정보입니다.",
                        "blockId" : "5e0df82cffa74800014bc838"
                    },
                ]
            }
        }
    cursor.close()
    conn.close()
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def restphoto(request):
    kind = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    if "식당" in kind:
        link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/food.jpg"
        string = "밥집 지도입니다."
    else:
        link = "https://raw.githubusercontent.com/jil8885/chatbot/release/hyuabot/templates/cafe.jpg"
        string = "카페 지도입니다."
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleImage":
                     {"imageUrl": link, "altText": string}
                 }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def phone_search(request):
    keyword = json.loads(request.body.decode("utf-8"))["action"]["params"]["searchkeyword"]
    string = phonesearch(keyword)
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText":
                     {"text": string}
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def update_campus(request):
    user = json.loads(request.body.decode("utf-8"))["userRequest"]["user"]['id']
    location = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    conn_sql = "host='" + os.getenv("dbhost") + "' dbname=" + os.getenv("dbname") + " user='" + os.getenv("dbuser") + "' password='" + os.getenv("dbpassword") + "'"
    conn = psycopg2.connect(conn_sql)
    cursor = conn.cursor()
    sql = "select * from userinfo where id=%s"
    cursor.execute('create table if not exists userinfo (id text, campus text)')
    cursor.execute(sql,(user,))
    userinfo = cursor.fetchall()
    if userinfo == []:
        if "서울" in location or "ERICA" in location:
            sql = "INSERT INTO userinfo (id, campus) values (%s, %s)"
            if "서울" in location:
                cursor.execute(sql, (id, 1))
                conn.commit()
                responseBody = {"version": "2.0",
                "template": {
                    "outputs": [
                        {"simpleText":
                            {"text": '서울캠퍼스로 전환되었습니다.'}
                            }]
                    }
                }
            else:
                cursor.execute(sql, (id, 0))
                conn.commit()
                responseBody = {"version": "2.0",
                "template": {
                    "outputs": [
                        {"simpleText":
                            {"text": 'ERICA캠퍼스로 전환되었습니다.'}
                            }]
                    }
                }
            return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
        else:
            responseBody = {"version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": '캠퍼스를 지정해주십시오'}
                    }
                ],
                "quickReplies":[
                    {
                        "action" : "block",
                        "label" : "🏫 서울",
                        "messageText" : "서울캠퍼스로 전환되었습니다.",
                        "blockId" : "5eaa9bf741559f000197775d"
                    },
                    {
                        "action" : "block",
                        "label" : "🏫 ERICA",
                        "messageText" : "ERICA 캠퍼스로 전환되었습니다.",
                        "blockId" : "5eaa9bf741559f000197775d"
                    }
                ]
            }
        }
    elif userinfo[0][1] == '0':
        sql = "update userinfo set='1' where id=%s"
        cursor.execute(sql, (user,))
        conn.commit()
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": '서울 캠퍼스로 전환되었습니다.'}
                    }
                ]
            }
        }
    elif userinfo[0][1] == '1':
        sql = "update userinfo set='0' where id=%s"
        cursor.execute(sql, (user,))
        conn.commit()
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText":
                        {"text": 'ERICA 캠퍼스로 전환되었습니다.'}
                    }
                ]
            }
        }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})