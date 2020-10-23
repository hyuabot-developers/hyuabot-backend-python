from enum import Enum
import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring
from firebase_admin import _apps, initialize_app, get_app, firestore
from datetime import datetime

from common.config import korea_timezone
from firebase.firebase_init import get_cred


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


def get_cafeteria_menu(cafeteria, url="https://www.hanyang.ac.kr/web/www/re", campus=0):
    now = datetime.now(tz=korea_timezone)
    cafeteria_info = {"restaurant": cafeteria.name}
    # get
    res = requests.get(f"{url}{cafeteria.value}")

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

    found = False
    menu_query = db.collection('cafeteria').where('name', '==', cafeteria.name)

    for cafeteria in menu_query.stream():
        found = True
        doc = cafeteria.to_dict()

    if found:
        last_used = doc['last_used']
        if (now.year, now.month, now.day) != (last_used.year, last_used.month, last_used.day):
            crawl = get_cafeteria_menu(cafeteria, campus=campus)
            crawl['last_used'] = now
            doc.update(crawl)
        else:
            return doc
    else:
        crawl = get_cafeteria_menu(cafeteria, campus=campus)
        crawl['last_used'] = now
        doc = db.collection('cafeteria').document(cafeteria.name)
        doc.set(crawl)

    return crawl
