import requests
from bs4 import BeautifulSoup, ResultSet

url = "https://rocket-league.com/trading?filterItem=2615&filterCertification=0&filterPaint=0&filterPlatform=1" \
      "&filterSearchType=2&filterItemType=0&p={0} "


class Item:
    def __init__(self, name, color=None, quantity=None):
        self.name = name
        if self.name != "Credits":
            self.color = color
        else:
            self.color = None
        if quantity is not None:
            self.quantity = int(quantity)
        else:
            self.quantity = 1

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.name, self.color, self.quantity).replace('\n', ' ')


class Offer:
    def __init__(self, have=None, want=None):
        if want is None:
            want = []
        if have is None:
            have = []
        self.want = want
        self.have = have

    def __repr__(self):
        return "(H: {0}, W: {1})".format(self.have, self.want)


def get_raw_offers(page: int = 0) -> ResultSet:
    page = requests.get(url.format(page)).text

    soup = BeautifulSoup(page, 'html.parser')
    offers = soup.findAll("div", {"class": "rlg-trade-display-container is--user"})
    return offers


def get_item_object(raw_item) -> Item:
    name = raw_item.img['alt']
    color = raw_item.find("div", {"class": "rlg-trade-display-item-paint"})
    if color is not None:
        color = color['data-name']
    quantity = raw_item.find("div", {"class": "rlg-trade-display-item__amount is--premium wide"})
    if quantity is not None:
        quantity = quantity.text
    return Item(name, color, quantity)


def get_items_list(raw_half_offer):
    raw_items = raw_half_offer.findAll("div", {"class": "rlg-trade-display-item rlg-trade-display-item-read"})
    items = list()
    for raw_item in raw_items:
        items.append(get_item_object(raw_item))
    return items


def get_offer_object(raw_offer):
    raw_have = raw_offer.find(id='rlg-youritems')
    raw_want = raw_offer.find(id='rlg-theiritems')
    have = get_items_list(raw_have)
    want = get_items_list(raw_want)
    offer = Offer(have, want)
    return offer


def get_offers(page: int = 0):
    offers = []
    raw_offers = get_raw_offers(page)
    for raw_offer in raw_offers:
        offers.append(get_offer_object(raw_offer))
    return offers


def main():
    get_offers()


if __name__ == '__main__':
    main()
