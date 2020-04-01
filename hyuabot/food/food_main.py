import requests, os
from bs4 import BeautifulSoup
import datetime

def make_string_food(cafeteria):
    string = crawling(cafeteria)
    return string

def crawling(cafeteria, date=None):
    string=""
    campus = "BVRPhfbjvn"
    cafeterias = {"학생식당" : "LTI0MTE0NTE5", "창의인재원식당" : "LTI0MTEyNjM2", "교직원식당": "LTI0MTE2NDAw", "창업보육센터": "LTI0MTA4ODY0", "푸드코트" : "LTI0MTEwNzUx"}
    request_url = "https://bablabs.com/openapi/v1/campuses/" + campus + "/stores/" + cafeterias[cafeteria]
    today = datetime.datetime.now() + datetime.timedelta(hours=9)
    if not date:
        date = "%s-%s-%s"%(today.year, today.month, today.day)
    headers = {"Accesstoken" : os.getenv("bob")}
    params = {"date" : date}
    res = requests.get(request_url, headers=headers, params=params)
    menu_list = []
    menus = res.json()['store']['menus']
    # 시간별 조식, 중식, 석식을 나눔
    string += "%s년%s월%s일 "%(today.year, today.month, today.day)
    if today.hour < 10:
        string += "조식\n"
        for x in menus:
            if x['time'] == 0:
                menu_list += [x]
    elif today.hour < 15:
        string += "중식\n"
        for x in menus:
            if x['time'] == 1:
                menu_list += [x]
    elif today.hour < 19:
        string += "석식\n"
        for x in menus:
            if x['time'] == 2:
                menu_list += [x]
    else:
        string = ""
        day = today + datetime.timedelta(days=1)
        date = "%s-%s-%s"%(day.year, day.month, day.day)
        res = requests.get(request_url, headers=headers, params=params)
        menu_list = []
        menus = res.json()['store']['menus']
        string += "%s년%s월%s일 "%(day.year, day.month, day.day)
        if menus[0]['time'] == 0:
            string += "조식\n"
            for x in menus:
                if x['time'] == 0:
                    menu_list += [x]
        elif menus[0]['time'] == 1:
            string += "중식\n"
            for x in menus:
                if x['time'] == 1:
                    menu_list += [x]
        if menus[0]['time'] == 2:
            string += "석식\n"
            for x in menus:
                if x['time'] == 2:
                    menu_list += [x]
    # 식단이 없을 때
    if not menu_list:
        string += '식단이 제공되지 않습니다'
    for x in menu_list:
        if x['name'] != '':
            string += x['name'] + ' '
        try:
            string += str(x['price']) + '원\n'
        except:
            pass
        string += x["description"]
        string += '\n\n'
    if string[-1] == '\n':
        string = string[:-1]
    return string.strip()


