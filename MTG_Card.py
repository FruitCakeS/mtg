class MTG_Card(object):
    def __init__(self, parsed_json):
        self.name = ""
        self.number = ""
        self.printings = ""
        """
        self.mciNumber = ""
        self.foreignNames = ""
        self.artist = ""
        self.text = ""
        self.printings = ""
        self.cmc = ""
        self.rarity = ""
        self.imageName = ""
        self.rulings = ""
        self.layout = ""
        self.manaCost = ""
        self.type = ""
        self.id = ""
        self.types = ""
        self.legalities = ""
        self.originalType = ""
        self.toughness = ""
        self.colors = ""
        self.subtypes = ""
        self.flavor = ""
        self.colorIdentity = ""
        self.power = ""
        self.originalText = ""
        self.supertypes = ""
        self.releaseDate = ""
        self.source = ""
        self.multiverseid = ""
        self.watermark = ""
        self.reserved = ""
        self.names = ""
        self.loyalty = ""
        self.variations = ""
        self.starter = ""
        self.border = ""
        self.life = ""
        self.hand = ""
        self.timeshifted = ""
        """


        for key in parsed_json.keys():
            key = str(key)

            if key == "name":
                self.name = parsed_json[key].encode('utf-8')
            if key == "number":
                self.number = parsed_json[key]
            if key == "printings":
                printings = []
                for printing in parsed_json[key]:
                    printings.append(printing.encode('utf-8'))
                self.printings = printings
    def __repr__(self):
        return self.name + " " + self.number + " " + str(self.printings)

    def __str__(self):
        return self.name + " " + self.number + " " + str(self.printings)
