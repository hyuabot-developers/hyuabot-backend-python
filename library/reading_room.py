import json

import requests
from firebase_admin import _apps, initialize_app, get_app, firestore
from datetime import datetime

from common.config import korea_timezone
from firebase.firebase_init import get_cred


def get_reading_room_seat(campus, room_id='', as_json=False):
    now = datetime.now(tz=korea_timezone)
    if not _apps:
        cred = get_cred()
        initialize_app(cred)
    else:
        get_app()
    db = firestore.client()
    if room_id:
        if campus:
            doc = db.collection('reading_room').document('seoul').collection('rooms').document(room_id)
            total_room = doc.get().to_dict()
            doc = db.collection('reading_room').document('seoul')
            active_room = doc.get().to_dict()['active_room']
            active_room = [x for x in active_room if '미개방' not in active_room]
            return total_room, active_room
        else:
            doc = db.collection('reading_room').document('erica').collection('rooms').document(room_id)
            total_room = doc.get().to_dict()
            doc = db.collection('reading_room').document('erica')
            active_room = doc.get().to_dict()['active_room']
            active_room = [x for x in active_room if '미개방' not in active_room]
            return total_room, active_room
    else:
        if campus:
            doc = db.collection('reading_room').document('seoul')
            seat_query = doc.get().to_dict()
            last_used = seat_query['last_used'].astimezone(korea_timezone)
            if (now - last_used).seconds // 60 >= 2 and (now - last_used).days >= 0:
                try:
                    url = 'https://lib.hanyang.ac.kr/smufu-api/pc/1/rooms-at-seat'
                    res = requests.get(url)
                except requests.exceptions.RequestException as e:
                    return ''

                src = json.loads(res.text)
                total_room = src['data']['list']
                active_room = [x['name'] for x in total_room if x['isActive']]
                doc.update({'last_used': now, 'active_room': active_room})
                for reading_room in total_room:
                    try:
                        doc = db.collection('reading_room').document('seoul').collection('rooms').document(
                            reading_room['name'])
                        doc.update({'name': reading_room['name'], 'total': reading_room['total'],
                                    'isActive': reading_room['isActive'], 'activeTotal': reading_room['activeTotal'],
                                    'occupied': reading_room['occupied'], 'available': reading_room['available'],
                                    'last_used': now})
                    except:
                        doc = db.collection('reading_room').document('seoul').collection('rooms').document(
                            reading_room['name'])
                        doc.set({'name': reading_room['name'], 'total': reading_room['total'],
                                 'isActive': reading_room['isActive'], 'activeTotal': reading_room['activeTotal'],
                                 'occupied': reading_room['occupied'], 'available': reading_room['available'],
                                 'last_used': now})
                return total_room, active_room
            else:
                docs = db.collection('reading_room').document('seoul').collection('rooms').where('isActive', '==', True)
                active_room = []
                total_room = []
                for doc in docs.stream():
                    if '미개방' not in doc.id:
                        active_room.append(doc.id)
                        total_room.append(doc.to_dict())
                return total_room, active_room
        else:
            doc = db.collection('reading_room').document('erica')
            seat_query = doc.get().to_dict()
            last_used = seat_query['last_used'].astimezone(korea_timezone)
            if (now - last_used).seconds // 60 >= 2 and (now - last_used).days >= 0:
                try:
                    url = 'https://lib.hanyang.ac.kr/smufu-api/pc/2/rooms-at-seat'
                    res = requests.get(url)
                except requests.exceptions.RequestException as e:
                    return ''

                src = json.loads(res.text)
                total_room = src['data']['list']
                active_room = [x['name'] for x in total_room if x['isActive']]
                doc.update({'last_used': now, 'active_room': active_room})
                for reading_room in total_room:
                    try:
                        doc = db.collection('reading_room').document('erica').collection('rooms').document(
                            reading_room['name'])
                        doc.update({'name': reading_room['name'], 'total': reading_room['total'],
                                    'isActive': reading_room['isActive'], 'activeTotal': reading_room['activeTotal'],
                                    'occupied': reading_room['occupied'], 'available': reading_room['available'],
                                    'last_used': now})
                    except:
                        doc = db.collection('reading_room').document('erica').collection('rooms').document(
                            reading_room['name'])
                        doc.set({'name': reading_room['name'], 'total': reading_room['total'],
                                 'isActive': reading_room['isActive'], 'activeTotal': reading_room['activeTotal'],
                                 'occupied': reading_room['occupied'], 'available': reading_room['available'],
                                 'last_used': now})
                return total_room, active_room
            else:
                docs = db.collection('reading_room').document('erica').collection('rooms').where('isActive', '==', True)
                active_room = []
                total_room = []
                for doc in docs.stream():
                    if '미개방' not in doc.id:
                        active_room.append(doc.id)
                        total_room.append(doc.to_dict())
                return total_room, active_room
