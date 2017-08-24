from .util import basket_list
from .cart import Cart

def buy_processor(request):
	return {'buy_status': basket_list(request)}



def cart(request):
    return {'cart': Cart(request)}
