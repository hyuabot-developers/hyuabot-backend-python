from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import files from subdirectories (하위폴더에서 파일 임포트)
# from .transport.subway import subway_erica
# from .transport.bus import bus_request
from .transport.shuttle_main import shuttle_main, schoolbus_main
from .food.food_main import make_string_food
from .library.lib_main import crawling_lib
from .phone.phone_search import phonesearch
# from .food.food_main import make_string_food
import datetime, json
import requests

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
        response = response.split("의")[0]
    busstop = busstop_list[response]
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
                    "label" : "셔틀콕",
                    "messageText" : "셔틀콕의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc8ee82127558b7e6eba"
                },
                {
                    "action" : "block",
                    "label" : "한대앞역",
                    "messageText" : "한대앞역의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc97e82127558b7e6ebc"
                },
                {
                    "action" : "block",
                    "label" : "예술인A",
                    "messageText" : "예술인A의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc9f5f38dd4c34bad81b"
                },
                {
                    "action" : "block",
                    "label" : "기숙사",
                    "messageText" : "기숙사의 셔틀버스 도착정보입니다.",
                    "blockId" : "5cc3dc865f38dd4c34bad819"
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def food(request):
    store = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    if "의 식단입니다" in store:
        store = store.split("의 식단")[0]
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
                    "blockId" : "5cc3f5fe5f38dd4c34bad846"
                },
                {
                    "action" : "block",
                    "label" : "교직원식당",
                    "messageText" : "교직원식당의 식단입니다.",
                    "blockId" : "5cc3f606384c5508fceec58f"
                },
                {
                    "action" : "block",
                    "label" : "창업보육센터",
                    "messageText" : "창업보육센터의 식단입니다.",
                    "blockId" : "5cc3f617384c5508fceec593"
                },
                {
                    "action" : "block",
                    "label" : "푸드코트",
                    "messageText" : "푸드코트의 식단입니다.",
                    "blockId" : "5cc3f60e384c5508fceec591"
                },
                {
                    "action" : "block",
                    "label" : "창의인재원식당",
                    "messageText" : "창의인재원식당의 식단입니다.",
                    "blockId" : "5cc3f621384c5508fceec595"
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def library(request):
    location = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    if location == "열람실 정보":
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
                    "label" : "제1열람실",
                    "messageText" : "제1열람실의 좌석정보입니다.",
                    "blockId" : "5e0df84692690d0001fca6ae"
                },
                {
                    "action" : "block",
                    "label" : "제3열람실",
                    "messageText" : "제3열람실의 좌석정보입니다.",
                    "blockId" : "5e0df85592690d0001fca6b0"
                },
                {
                    "action" : "block",
                    "label" : "제4열람실",
                    "messageText" : "제4열람실의 좌석정보입니다.",
                    "blockId" : "5e0df86192690d0001fca6b2"
                },
                {
                    "action" : "block",
                    "label" : "제5열람실",
                    "messageText" : "제5열람실의 좌석정보입니다.",
                    "blockId" : "5e0df86a92690d0001fca6b4"
                }
            ]
        }
    }
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


def getLabel(x):
    buttonlabel=""
    if(x != ""):
        if "facebook" in x:
            if "videos" in x:
                buttonlabel = "페이스북 영상"
            else:
                buttonlabel = "페이스북 링크"
        elif "everytime" in x:
            buttonlabel = "에브리타임 링크"
        elif "naver.me" in x:
            buttonlabel = "네이버폼 지원서"
        elif "open.kakao.com" in x:
            buttonlabel = "카톡 오픈채팅"
        elif "google" in x or "goo.gl" in x or "http://bit.ly/2IygLil" or "forms.gle" in x:
            buttonlabel = "구글폼 지원서"
        else:
            buttonlabel = "기타링크"
    return buttonlabel


@csrf_exempt
def club(request):
    category = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    category_tojson = {
        "연행예술분과" : "performing", 
        "체육분과" : "physical", 
        "평면예술분과" : "drawing", 
        "학술분과" : "studying", 
        "구기체육분과" : "ball", 
        "봉사분과" : "volunteering", 
        "교양분과" : "culture", 
        "종교분과" : "religion", 
        "기타":"others"
        }
    link = "https://raw.githubusercontent.com/jil8885/ERICA_api/master/club.json"
    response = requests.get(link)
    body = response.json()
    result = body[category_tojson[category]]
    json_result = []
    thumbnail = False
    
    for x in result:
        if "photo" in x.keys():
            thumbnail = True
            break
    for x in list(result):
        json_item = {"title" : x["name"], "description" : x["description"]}
        if x["link"] != "":
            label = getLabel(x["link"])
            json_item["buttons"] = [{"action" : "webLink", "label" : label, "webLinkUrl" : x["link"]}]
        if "link2" in x.keys():
            label = getLabel(x["link2"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link2"]})
        if "link3" in x.keys():
            label = getLabel(x["link3"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link3"]})
        if "info" in x.keys():
            label = "상세정보 알아보기"
            blockId = "5e71907427fd9f0001351c81"
            json_item["buttons"].append({"action" : "block", "label" : label, "messageText": x["name"], "blockId" : blockId})
        if "photo" in x.keys():
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = x["photo"]
            if "width" in x.keys() and "height" in x.keys():
                json_item["thumbnail"]["fixedRatio"] = True
                json_item["thumbnail"]["width"] = x["width"]
                json_item["thumbnail"]["height"] = x["height"]
            
        json_result.append(json_item)
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def circle(request):
    category = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    category_tojson = {
        "소프트웨어":"software",
        "ICT융합":"ict",
        "소프트웨어융합대학":"soft",
        "전자공":"electric",
        "기계공":"mechanic",
        "로봇공":"robot",
        "공학대학":"engineering",
        "국제문화대학":"gukmun",
        "디자인대학":"design",
        "경상대학":"economy_college",
        "경영학부":"biz",
        "경제학부":"economy"
    }
    link = "https://raw.githubusercontent.com/jil8885/ERICA_api/master/circles.json"
    response = requests.get(link)
    body = response.json()
    result = body[category_tojson[category]]
    json_result = []
    thumbnail = False
    for x in result:
        if "photo" in x.keys():
            thumbnail = True
            break
    for x in result:
        json_item = {"title" : x["name"], "description" : x["description"]}
        if x["link"] != "":
            label = getLabel(x["link"])
            json_item["buttons"] = [{"action" : "webLink", "label" : label, "webLinkUrl" : x["link"]}]
        if "link2" in x.keys():
            label = getLabel(x["link2"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link2"]})
        if "link3" in x.keys():
            label = getLabel(x["link3"])
            json_item["buttons"].append({"action" : "webLink", "label" : label, "webLinkUrl" : x["link3"]})
        if "info" in x.keys():
            label = "상세정보 알아보기"
            blockId = "5e71907427fd9f0001351c81"
            json_item["buttons"].append({"action" : "block", "label" : label, "messageText": x["name"], "blockId" : blockId})
        if "photo" in x.keys():
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = x["photo"]
            if "width" in x.keys() and "height" in x.keys():
                json_item["thumbnail"]["fixedRatio"] = True
                json_item["thumbnail"]["width"] = x["width"]
                json_item["thumbnail"]["height"] = x["height"]
        elif thumbnail:
            json_item["thumbnail"] = {}
            json_item["thumbnail"]["imageUrl"] = "https://raw.githubusercontent.com/jil8885/djangoapp-kakao-i/master/templates/images/default.png"
            json_item["thumbnail"]["fixedRatio"] = True
            json_item["thumbnail"]["width"] = 833
            json_item["thumbnail"]["height"] = 833
        json_result.append(json_item)

    if category == "소프트웨어융합대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "소프트웨어",
                    "messageText" : "소프트웨어",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "ICT융합",
                    "messageText" : "ICT융합",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }              
        ]
    elif category == "공학대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "전자공",
                    "messageText" : "전자공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "기계공",
                    "messageText" : "기계공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "로봇공",
                    "messageText" : "로봇공",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }              
        ]
    elif category == "경상대학":
        quickReplies = [
                {
                    "action" : "block",
                    "label" : "경제학부",
                    "messageText" : "경제학부",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                },
                {
                    "action" : "block",
                    "label" : "경영학부",
                    "messageText" : "경영학부",
                    "blockId" : "5e70be9a2d3cd0000121a234"
                }           
        ]        
    else:
        quickReplies = []
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    if quickReplies != []:
        responseBody["template"]["quickReplies"] = quickReplies
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})

@csrf_exempt
def info(request):
    name = json.loads(request.body.decode("utf-8"))["userRequest"]["utterance"]
    name_tofolder = {
        "CRUX":"CRUX"
    }
    clubName = name_tofolder[name]
    json_result = []
    if clubName == "CRUX":
        json_result.append({"title" : clubName + "에서는?", "description" : "❗⚠️국제문화대학 신입생 친구들 주목⚠️❗\n\n안녕하세요! [국제문화대학 밴드동아리 CRUX]에서 신입부원을 모집합니다🥳\n\n⬇️모집 대상⬇️\n\n🎤 밴드에 관심이 많으신 분\n🎤 기타,드럼,베이스,키보드 등의 악기 연주를 좋아하시는 분\n🎤 공연을 해보고 싶으신 분\n🎤 국문대 인싸가 되고싶으신 분"})
        json_result.append({"title" : clubName + "에서는?", "description" : "⬇️동아리 활동⬇️\n\n🥁 1년에 2번 정기공연 및 여름방학 홍대공연\n🥁 매주 목요일 정기모임 및 뒤풀이\n🥁 각 세션별 멘토링\n🥁 상상유니브 보컬 클래스\n🥁 매 학기 신나는 MT\n🥁 기타 다양한 외부 행사\n\n기타,드럼,베이스,보컬,키보드 5개 세션의 신입부원을 모집하오니 가입신청을 원하시는 분들은 아래 네이버폼을 작성해 주시면 감사하겠습니다🤩🤩", "buttons":[{"action" : "webLink", "label" : "지원서 링크", "webLinkUrl" : "http://naver.me/xqGnPF58"}]})
        for x in range(1, 9):
            json_result.append({"thumbnail":{"imageUrl" : "https://raw.githubusercontent.com/jil8885/djangoapp-kakao-i/master/templates/images/club/CRUX/CRUX" + str(x) + ".jpeg"}})  
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                    "type": "basicCard",
                    "items":json_result
                    }
                }
            ]
        }
    }
    return JsonResponse(responseBody, json_dumps_params = {'ensure_ascii': False})
