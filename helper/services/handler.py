
import pyrebase

from helper import db
import json
from helper.models import Character
from random import randint

import ast

class Handler:

    @staticmethod
    def push_data(data, child:str):
        try:
            db.child(child.capitalize()).push(data)
            return 1
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0

    @staticmethod
    def update_data(data, child:str, name:str):
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                if(entity.val()['name'] == name.lower()):
                    db.child(child.capitalize()).child(entity.key()).update(data)
            return 1
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0

    @staticmethod
    def delete_data(child: str, keyid: str):
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                print(entity.val()['keyid'])
                if (entity.val()['keyid'] == name.lower()):
                    db.child(child.capitalize()).child(entity.key()).remove()
            return 1
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0

    @staticmethod
    def delete_character(child: str, name: str, userUID: str):
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                if (entity.val()['name'] == name and entity.val()['userUID']==userUID):
                    db.child(child.capitalize()).child(entity.key()).remove()
            return 1
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0

    @staticmethod
    def read_data(child: str):
        try:
            database = db.child(child).get()
            for entity in database.each():
                print("\t" + entity.key() + " : ")
                print("\t" + str(entity.val()))
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0
            


    @staticmethod
    def get_data_by_uid(request :str, child: str):
        items = []
        uid = str(request.session['uid'])
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                if entity.val()['userUID'] == uid:
                    items.append(entity.val())
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0
        return items

    @staticmethod
    def get_data(child: str):
        items = []
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                items.append(entity.val())
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0
        return items

    @staticmethod
    def get_data_in_list(child: str):
        data: list = []
        try:
            database = db.child(child.capitalize()).get()
            for entity in database.each():
                data.append(tuple(((entity.val()['name']), (entity.val()['name']))))
            return data
        except:
            print(Handler.__name__ + ": something went wrong")
            return 0

    @staticmethod
    def session_handler(request, user):
        request.session['uid']=str(user['localId'])
        request.session['email']=str(user['email'])

    @staticmethod
    def user_exists(request):
        try: 
            request.session['uid']
        except:
            return False
        else:
            return True

    @staticmethod
    def get_primary_statistics(obj):
        primaryNames = ["WS", "BS", "S", "T", "AG", "INT", "WP", "FEL"]
        primaryStatistics = {}
        if(type(obj) == dict):
            for i in range(0, 8):
                primaryCell = obj['primaryStatistics'][i * 2] + obj['primaryStatistics'][(i * 2) + 1]
                primaryStatistics[primaryNames[i]]= primaryCell
        if(type(obj) == str):
            for i in range(0, 8):
                primaryCell = obj[i * 2] + obj[(i * 2) + 1]
                primaryStatistics[primaryNames[i]]= primaryCell

        return primaryStatistics

    @staticmethod
    def get_secondary_statistics(obj):
        secondaryNames = ["A", "W", "SB", "TB", "M", "MAG", "IP", "FP"]
        secondaryStatistics = {}
        if(type(obj) == dict):
            for i in range(0, 8):
                secondaryCell = obj['secondaryStatistics'][i * 2] + obj['secondaryStatistics'][(i * 2) + 1]
                secondaryStatistics[secondaryNames[i]]= secondaryCell
        if(type(obj) == str):
            for i in range(0, 8):
                secondaryCell = obj[i * 2] + obj[(i * 2) + 1]
                secondaryStatistics[secondaryNames[i]]= secondaryCell
        return secondaryStatistics

    def race_allowance(race, availableFor):
        index = 0
        # Get index
        for entity in Handler.get_data("Races"):
            if race != entity["name"]:
                index += 1
            else:
                break
        # Check if allowed
        if availableFor[index-1] == "1":
            return True
        else:
            return False

    @staticmethod
    def get_all_allowed_professions(professions, race):
        list = []
        for entity in professions:
            if Handler.race_allowance(race, entity["availableFor"]):
                list.append(tuple((entity["name"], entity["name"])))
        return list

    @staticmethod
    def roll():
        stats = ""
        for i in range(0, 8):
            number = randint(1, 20)
            if number < 10:
                number = "0" + str(number)
            stats += str(number)
        return stats

    def stat_roll():
        stats = ""
        for i in range(0, 8):
            number = randint(1, 20)
            if number < 10:
                number = "0" + str(number)
            stats += str(number)
        return stats


    @staticmethod
    def get_merged_primary(race_name):
        stats = ""
        for entity in Handler.get_data("Races"):
            if entity["name"] == race_name:
               stats = int(Handler.stat_roll()) + int(entity["primaryStatistics"])
        stats = str(stats)
        while len(stats) < 16:
            stats = "0" + stats
        return stats

    @staticmethod
    def vitality_roll(race_name):
        vitality = ""
        number = randint(0, 3)
        for entity in Handler.get_data("Races"):
            if entity["name"] == race_name:
                vitality += (entity['wRoll'][number*2] + entity['wRoll'][number*2+1])
        return vitality

    @staticmethod
    def fp_roll(race_name):
        fp = ""
        number = randint(0, 2)
        for entity in Handler.get_data("Races"):
            if entity["name"] == race_name:
               fp += "0" + entity['fpRoll'][number]
        return fp
    
    @staticmethod
    def get_merged_secondary(race_name, primary):
        stats = ""
        for entity in Handler.get_data("Races"):
            if entity["name"] == race_name:
                stats = entity["secondaryStatistics"]
        # Rulebook changes
        addition = "00" \
                   + Handler.vitality_roll(race_name) + "0" \
                   + primary[4] + "0" \
                   + primary[6] + "000000" + Handler.fp_roll(race_name)
        stats = int(stats) + int(addition)

        stats = str(stats)
        while len(stats) < 16:
            stats = "0" + stats

        return stats

    @staticmethod
    def get_inventory(race_name):
        dict = {}
        for entity in Handler.get_data("Professions"):
            if entity["name"] == race_name:
                dict['equipment'] = entity['equipment']
                dict['weapon'] = entity['weapon']
                dict['armor'] = entity['armor']
        return dict