
import urllib
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):

    in_row = False
    column_count = 0
    in_card_name = False
    in_price = False
    prices = []
    card_name = ""
    price = ""

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_row = True
        if self.in_row and tag == "td":
            self.column_count += 1
            if self.column_count == 1:
                self.in_card_name = True
            else:
                self.in_card_name = False
            if self.column_count == 4:
                self.in_price = True
            else:
                self.in_price = False

    def handle_endtag(self, tag):
        if tag == "tr":
            self.in_row = False
            self.column_count = 0
            if self.card_name != "" and self.price != "":
                stripped_price = self.price.strip().replace(",","")
                fprice = float(stripped_price)
                self.prices.append([self.card_name.strip().lower(), fprice])
            self.card_name = ""
            self.price = ""
        if tag == "td":
            self.in_card_name = False
            self.in_price = False

    def handle_data(self, data):
        if self.in_card_name:
            self.card_name+=data
        if self.in_price:
            self.price += data

    def getOutput(self):
        return self.prices

    def clear_prices(self):
        self.in_row = False
        self.column_count = 0
        self.in_card_name = False
        self.in_price = False
        self.prices = []
        self.card_name = ""
        self.price = ""



def fetch_prices(set, online, foil):
    f = ""
    if foil:
        f = "_F"
    o = "online"
    if not online:
        o = "paper"

    url = "https://www.mtggoldfish.com/index/"+set+f+"#"+o
    f = urllib.urlopen(url)
    html = f.read()
    table_index = html.find("<table class='table table-bordered table-condensed tablesorter tablesorter-bootstrap-popover-"+o)
    if table_index != -1:
        html = html[table_index:]
        table_end_index = html.find("</table>")
        html = html[:table_end_index+8]
        parser = MyHTMLParser()
        parser.clear_prices()
        parser.feed(html)
        return parser.getOutput()
    return []
