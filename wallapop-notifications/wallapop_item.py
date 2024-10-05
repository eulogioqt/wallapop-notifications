class WallapopItem:

    def __init__(self, title, price, link):
        self.title = title
        self.price = price
        self.link = link

    def __eq__(self, other):
        if isinstance(other, WallapopItem):
            return (self.title == other.title and
                    self.price == other.price and
                    self.link == other.link)
        return False

    def __str__(self):
        return f"Title: {self.title} | Price: {self.price} | Link: {self.link}"
