from enum import Enum
import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring
from firebase_admin import _apps, initialize_app, get_app, firestore
from datetime import datetime

from common.config import korea_timezone
from firebase.firebase_init import get_cred
from google.cloud.exceptions import NotFound


class CafeteriaSeoul(Enum):
    student_seoul_1 = "1"
    teacher_seoul_1 = "2"
    sarang_seoul = "3"
    teacher_seoul_2 = "4"
    student_seoul_2 = "5"
    dorm_seoul_1 = "6"
    dorm_seoul_2 = "7"
    hangwon_seoul = "8"


class CafeteriaERICA(Enum):
    teacher_erica = "11"
    student_erica = "12"
    dorm_erica = "13"
    foodcoart_erica = "14"
    changbo_erica = "15"


class Restaurant:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def get_cafeteria_menu(cafeteria=None, restaurant=None, url="https://www.hanyang.ac.kr/web/www/re"):
    now = datetime.now(tz=korea_timezone)

    if cafeteria:
        cafeteria_info = {"restaurant": cafeteria.name}
        # get
        res = requests.get(f"{url}{cafeteria.value}")
    else:
        cafeteria_info = {"restaurant": restaurant.name}
        res = requests.get(f"{url}{restaurant.value}")

    tree = fromstring(res.text)
    inboxes = CSSSelector("div.tab-pane")
    td = CSSSelector("td")

    for inbox in inboxes(tree):
        for content in td(inbox):
            txt = content.text_content().strip()
            cafeteria_info['time'] = ''
            if '조식' in txt:
                cafeteria_info['time'] += f'{txt}\n'
            elif '중식' in txt:
                cafeteria_info['time'] += f'{txt}\n'
            elif '석식' in txt:
                cafeteria_info['time'] += f'{txt}\n'
    inboxes = CSSSelector("div.in-box")
    h4 = CSSSelector("h4")  # 조식, 중식, 석식
    h3 = CSSSelector("h3")  # menu
    li = CSSSelector("li")
    price = CSSSelector("p.price")
    for inbox in inboxes(tree):
        title = h4(inbox)[0].text_content()
        cafeteria_info[title] = []
        for l in li(inbox):
            if h3(l):
                menu = h3(l)[0].text_content().replace("\t", "").replace("\r\n", "")
                p = price(l)[0].text_content()
            cafeteria_info[title].append({"menu": menu, "price": p})

    return cafeteria_info


def get_recipe(cafeteria, url="https://www.hanyang.ac.kr/web/www/re", campus=0):
    now = datetime.now(tz=korea_timezone)
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()

    menu_query = db.collection('cafeteria').document(cafeteria.name)
    try:
        doc = menu_query.get()
        if not doc.to_dict():
            crawl = get_cafeteria_menu(cafeteria)
            crawl['last_used'] = now
            doc = db.collection('cafeteria').document(cafeteria.name)
            doc.set(crawl)
        else:
            last_used = doc.to_dict()['last_used']
            if (now.year, now.month, now.day) != (last_used.year, last_used.month, last_used.day):
                crawl = get_cafeteria_menu(cafeteria)
                crawl['last_used'] = now
                menu_query.update(crawl)
            else:
                return doc.to_dict()

    except NotFound:
        crawl = get_cafeteria_menu(cafeteria)
        crawl['last_used'] = now
        doc = db.collection('cafeteria').document(cafeteria.name)
        doc.set(crawl)

    return crawl


def update_recipe():
    now = datetime.now(tz=korea_timezone)
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()

    restaurant_list = {"student_seoul_1": "1", "teacher_seoul_1": "2", "sarang_seoul": "3", "teacher_seoul_2": "4",
                       "student_seoul_2": "5", "dorm_seoul_1": "6", "dorm_seoul_2": "7", "hangwon_seoul": "8",
                       "teacher_erica": "11", "student_erica": "12", "dorm_erica": "13", "foodcoart_erica": "14",
                       "changbo_erica": "15"}
    for _, (key, value) in enumerate(restaurant_list.items()):
        restaurant_list = Restaurant(key, value)
        recipe = get_cafeteria_menu(restaurant=restaurant_list)

        doc = db.collection('cafeteria').document(key)
        try:
            snapshot = doc.get()
            if not snapshot.to_dict():
                recipe['last_used'] = now
                doc.set(recipe)
            else:
                doc.update(recipe)
        except NotFound:
            recipe['last_used'] = now
            doc.set(recipe)
