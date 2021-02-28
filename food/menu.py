import os
from copy import deepcopy
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
    food_court_erica = "14"
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


def get_recipe_all_cafeteria(language: str):
    now = datetime.now(tz=korea_timezone)
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()

    menu_collection = db.collection(f'cafeteria_{language}').stream()
    result = {}
    for doc in menu_collection:
        try:
            if not doc.to_dict():
                crawl = get_cafeteria_menu(doc.id)
                crawl['last_used'] = now
                doc = db.collection(f'cafeteria_{language}').document(doc.id)
                doc.set(crawl)
                result[doc.id] = crawl
            else:
                result[doc.id] = doc.to_dict()

        except NotFound:
            crawl = get_cafeteria_menu(doc.id)
            crawl['last_used'] = now
            doc = db.collection(f'cafeteria_{language}').document(doc.id)
            doc.set(crawl)

            result[doc.id] = crawl
    return result


def get_recipe(cafeteria):
    now = datetime.now(tz=korea_timezone)
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()

    menu_query = db.collection('cafeteria_ko').document(cafeteria.name)
    try:
        doc = menu_query.get()
        if not doc.to_dict():
            crawl = get_cafeteria_menu(cafeteria)
            crawl['last_used'] = now
            doc = db.collection('cafeteria_ko').document(cafeteria.name)
            doc.set(crawl)
        else:
            return doc.to_dict()

    except NotFound:
        crawl = get_cafeteria_menu(cafeteria)
        crawl['last_used'] = now
        doc = db.collection('cafeteria_ko').document(cafeteria.name)
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
    # languages = ['ko', 'en', 'zh-CN']
    languages = ['ko']
    restaurant_list = {"student_seoul_1": "1", "teacher_seoul_1": "2", "sarang_seoul": "3", "teacher_seoul_2": "4",
                       "student_seoul_2": "5", "dorm_seoul_1": "6", "dorm_seoul_2": "7", "hangwon_seoul": "8",
                       "teacher_erica": "11", "student_erica": "12", "dorm_erica": "13", "food_court_erica": "14",
                       "changbo_erica": "15"}

    for _, (key, value) in enumerate(restaurant_list.items()):
        restaurant_list = Restaurant(key, value)
        recipe = get_cafeteria_menu(restaurant=restaurant_list)

        for language in languages:
            doc = db.collection(f'cafeteria_{language.split("-")[0]}').document(key)
            recipe_translated = deepcopy(recipe)
            if language != 'ko':
                kinds = [x for x in recipe_translated.keys() if "식" in x]
                for kind in kinds:
                    for menu in recipe_translated[kind]:
                        menu['menu'] = get_translated_menu(menu['menu'], language)
            try:
                snapshot = doc.get()
                recipe_translated['last_used'] = now
                menu_keys = ["조식", "중식", "석식"]
                for key in menu_keys:
                    if key not in recipe_translated.keys():
                        recipe_translated[key] = []
                if not snapshot.to_dict():
                    doc.set(recipe_translated)
                else:
                    doc.update(recipe_translated)
            except NotFound:
                recipe_translated['last_used'] = now
                doc.set(recipe_translated)


def get_translated_menu(menu: str, lang: str):
    if not menu:
        return ''
    requests_url = "https://openapi.naver.com/v1/papago/n2mt"
    req = requests.post(requests_url, headers={'X-Naver-Client-Id': os.getenv('papago_client_id'),
                                               'X-Naver-Client-Secret': os.getenv('papago_client_secret')},
                        data={'source': 'ko', 'target': lang, 'text': menu})
    try:
        return req.json()['message']['result']['translatedText']
    except KeyError:
        return menu
