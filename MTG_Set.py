class MTG_Set(object):
	def __init__(self, json):
		self.code = "" #gathere code
		self.name = "" #set name
		self.mkm_name = "" #mkm short
		self.mkm_id = "" #mkm short
		self.border = "" #white/black/silver
		self.translations = "" #?
		self.releaseDate = "" #?
		self.booster = "" #?
		self.type = "" #expansion/core/starter/promo
		self.block = ""
		self.magicRaritiesCodes = ""
		self.magicCardsInfoCode = ""
		self.gathererCode = ""
		self.oldCode = ""
		self.onlineOnly = ""
		self.alternativeNames = ""
		self.cards = ""

		for key in json.keys():
			key = str(key)
			if key!="cards":
				print key+" "+unicode(json[key])

			if key == "code":
				self.code = json[key]
			if key == "name":
				self.name = json[key].encode('utf-8')
			if key == "mkm_name":
				self.mkm_name = json[key]
			if key == "mkm_id":
				self.mkm_id = json[key]
			if key == "border":
				self.border = json[key]
			if key == "translations":
				self.translations = json[key]
			if key == "releaseDate":
				self.releaseDate = json[key]
			if key == "booster":
				self.booster = json[key]
			if key == "type":
				self.type = json[key]
			if key == "block":
				self.block = json[key]
			if key == "magicCardsInfoCode":
				self.magicCardsInfoCode = json[key]
			if key == "magicRaritiesCodes":
				self.magicRaritiesCodes = json[key]
			if key == "gathererCode":
				self.gathererCode = json[key]
			if key == "oldCode":
				self.oldCode = json[key]
			if key == "onlineOnly":
				self.onlineOnly = json[key]
			if key == "alternativeNames":
				self.alternativeNames = json[key]

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
