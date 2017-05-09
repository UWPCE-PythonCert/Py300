# Blueprint for making Car object

class Car():
    """A vehicle at Car Wrecks Awesome Car Lot.
"""
    wheels = 4  # class attribute

    def __init__(self, model, price):
        """Return a Car object whose model is *model* and current price is *price*."""
        self.model = model # instance attribute
        self.price = price

    def appreciate(self, amount):
        """In the unlikely event the value appreciates..."""
        self.price += amount
        return self.price

    def sale(self, discount):
        """Return the new price after applying the discount.
        Discount should be in decimal form: 0.30 for 30% off"""
        self.price *= discount
        return self.price

    @staticmethod
    def honk():
        # method not dependent on object or its attributes, so can be 
        # static. 
        print('beep, beep!')

    @classmethod
    def is_motorcycle(cls):
        return cls.wheels == 2

    # What happens if we eliminate self.price from __init__ and just
    # set it here?
    #def set_price(price):
    #    self.price = price

# to create a Car object:
car301 = Car('Celica', 100.00)

# Accessing class attributes:
#print('instantiated car {} wheels'.format(car301.wheels))
#print('car class {} wheels'.format(Car.wheels))


