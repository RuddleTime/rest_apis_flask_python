class Store:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, name, price):
        self.items.append({
            'name': name,
            'price': price
        })

    def stock_price(self):
        total = 0
        for item in self.items:
            total += item['price']
        return total

    @classmethod
    def franchise(cls, store):
        # Return another store, with the same name as the argument's name, plus " - franchise"
        return cls(store.name + ' - franchise')

    @staticmethod
    def store_details(store):
        # Return a string representing the argument
        # It should be in the format 'NAME, total stock price: TOTAL'
        return "{0}, total stock price: {1}".format(store.name, store.stock_price())


cvs = Store('Test')
cvs.add_item('cat', 100)
cvs.add_item('cat', 10)
print(cvs.name)
print(cvs.items)
print(cvs.stock_price())


new_store = Store.franchise(cvs)
print(new_store.name)
print(new_store.stock_price())
print(Store.store_details(cvs))
