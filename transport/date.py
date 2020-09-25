from firebase_admin import firestore
from datetime import datetime

def get_date(modified=False):
    now = datetime.now()

    if modified:
        pass
    else:
        if (now >= datetime.strptime(f'{now.year}-03-01', '%Y-%m-%d') and now <= datetime.strptime(f'{now.year}-06-21', '%Y-%m-%d')) or (now >= datetime.strptime(f'{now.year}-09-01', '%Y-%m-%d') and now <= datetime.strptime(f'{now.year}-12-21', '%Y-%m-%d')):
            print("semester")
        elif if (now >= datetime.strptime(f'{now.year}-03-01', '%Y-%m-%d') and now <= datetime.strptime(f'{now.year}-06-21', '%Y-%m-%d')) or (now >= datetime.strptime(f'{now.year}-09-01', '%Y-%m-%d') and now <= datetime.strptime(f'{now.year}-12-21', '%Y-%m-%d')):