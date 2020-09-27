import firebase_admin


def get_cred():
    cred = firebase_admin.credentials.ApplicationDefault()
    # cred = firebase_admin.credentials.Certificate('Z:\\Firebase auth\\personal-sideprojects-firebase-adminsdk.json')
    return cred
