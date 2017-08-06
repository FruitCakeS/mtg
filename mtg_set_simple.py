class MTG_Set_Simple(object):
    def __init__(self, json):
        self.code = "" #gathere code
        self.name = "" #set name
        self.type = "" #expansion/core/starter/promo
        self.cards = ""

        for key in json.keys():
            key = str(key)
            if key!="cards":
                print key+" "+unicode(json[key])

            if key == "code":
                self.code = json[key]
            if key == "name":
                self.name = json[key].encode('utf-8')
            if key == "type":
                self.type = json[key]
            if key == "cards":
                self.cards = json[key]
        print ""
        """
        if ("code" in json.keys()):
            print "code"+" "+json["code"]
        if ("name" in json.keys()):
            print "name"+" "+json["name"]
        if ("mkm_name" in json.keys()):
            print "mkm_name"+" "+json["mkm_name"]
        if ("mkm_name" in json.keys()):
            print "mkm_name"+" "+json["mkm_name"]
        """
