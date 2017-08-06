import json
from MTG_Card import *
class MTG_Set(object):
    def __init__(self, parsed_json):
        self.code = "" #gathere code
        self.name = "" #set name
        self.type = "" #expansion/core/starter/promo
        self.cards = ""
        
        other="""
        self.mkm_name = "" #mkm short
        self.mkm_id = "" #mkm short
        self.border = "" #white/black/silver
        self.translations = "" #?
        self.releaseDate = "" #?
        self.booster = "" #?
        
        self.block = ""
        self.magicRaritiesCodes = ""
        self.magicCardsInfoCode = ""
        self.gathererCode = ""
        self.oldCode = ""
        self.onlineOnly = ""
        self.alternativeNames = ""
        """

        for key in parsed_json.keys():
            key = str(key)
            #if key!="cards":
                #print key+" "+unicode(parsed_json[key])

            if key == "code":
                self.code = parsed_json[key]
            if key == "name":
                self.name = parsed_json[key].encode('utf-8')
            if key == "cards":
                cards = parsed_json[key]
                self.cards = []
                for card in cards:
                    self.cards.append(MTG_Card(card))
            if key == "type":
                self.type = parsed_json[key]

            """
            if key == "mkm_name":
                self.mkm_name = parsed_json[key]
            if key == "mkm_id":
                self.mkm_id = parsed_json[key]
            if key == "border":
                self.border = parsed_json[key]
            if key == "translations":
                self.translations = parsed_json[key]
            if key == "releaseDate":
                self.releaseDate = parsed_json[key]
            if key == "booster":
                self.booster = parsed_json[key]
            
            if key == "block":
                self.block = parsed_json[key]
            if key == "magicCardsInfoCode":
                self.magicCardsInfoCode = parsed_json[key]
            if key == "magicRaritiesCodes":
                self.magicRaritiesCodes = parsed_json[key]
            if key == "gathererCode":
                self.gathererCode = parsed_json[key]
            if key == "oldCode":
                self.oldCode = parsed_json[key]
            if key == "onlineOnly":
                self.onlineOnly = parsed_json[key]
            if key == "alternativeNames":
                self.alternativeNames = parsed_json[key]
            """
            
        print ""
        """
        if ("code" in parsed_json.keys()):
            print "code"+" "+parsed_json["code"]
        if ("name" in parsed_json.keys()):
            print "name"+" "+parsed_json["name"]
        if ("mkm_name" in parsed_json.keys()):
            print "mkm_name"+" "+parsed_json["mkm_name"]
        if ("mkm_name" in parsed_json.keys()):
            print "mkm_name"+" "+parsed_json["mkm_name"]
        """
