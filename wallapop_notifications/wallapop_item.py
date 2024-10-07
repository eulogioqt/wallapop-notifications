class WallapopItem:

    def __init__(self, title, price, link):
        self.title = title
        self.price = price
        self.link = link

    def __eq__(self, other):
        if not isinstance(other, WallapopItem):
            return False
        
        return self.title == other.title and  self.price == other.price and self.link == other.link

    def __str__(self):
        return f"{self.title} ({self.price})"

    def is_empty(self):
        return len(self.title) + len(self.price) + len(self.link) == 0