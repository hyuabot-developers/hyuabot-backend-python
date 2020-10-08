import firebase_admin


def get_cred():
    cred = firebase_admin.credentials.ApplicationDefault()
    return cred
