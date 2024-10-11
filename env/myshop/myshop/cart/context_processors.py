from .cart import Cart

def cart(requet):
    return {'cart': Cart(requet)}
