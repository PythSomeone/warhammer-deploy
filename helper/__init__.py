import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import pyrebase
import json

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://warhammerhelper-64ecf-default-rtdb.europe-west1.firebasedatabase.app/'})
#firebase=pyrebase.initialize_app(json.loads('firebase-sdk.json'))

with open('pyrebase-sdk.json') as json_file:
    pyrecred = json.loads(json_file.read())
firebase=pyrebase.initialize_app(pyrecred)
db = firebase.database()
authe=firebase.auth()
