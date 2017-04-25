# a couple of fake functions to get shirt prices
# all stores stock t-shirts and dress shirts
# create a decorator that allows you to compare prices

# hint: use the fact that decorators are run at import time
# this decorator does not need to be a closure

comparator = []

def buy_from_boutique(shirt_type):
    if shirt_type is 't-shirt':
        return 50, 'boutique'
    else:
        return 100, 'boutique'

def buy_from_department_store(shirt_type):
    if shirt_type is 't-shirt':
        return 20, 'dept'
    else:
        return 50, 'dept'

def buy_from_box_store(shirt_type):
    if shirt_type is 't-shirt':
        return 10, 'box'
    else:
        return 30, 'box'

def buy_from_thrift_store(shirt_type):
    if shirt_type is 't-shirt':
        return 1, 'thrift'
    else:
        return 3, 'thrift'
    

# will need a non-decorated function to compare prices
# this function will take advantage of the fact that 
# all of these functions have the same signature.
# which store gives you the best price, and what is it?
