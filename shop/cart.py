# -*- coding: utf-8 -*-
from decimal import Decimal
from django.conf import settings
from shop.models import Flower 

class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товара в корзину пользователя или обновление количеста товара
    def add(self, flower, quantity=1, update_quantity=False):
        flower_id = str(flower.id)
        if flower_id not in self.cart:
            self.cart[flower_id] = {'quantity': 0,
                                     'price': str(flower.price)}
        if update_quantity:
            self.cart[flower_id]['quantity'] = quantity
        else:
            self.cart[flower_id]['quantity'] += quantity
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, flower):
        flower_id = str(flower.id)
        if flower_id in self.cart:
            del self.cart[flower_id]
            self.save()

    # Итерация по товарам
    def __iter__(self):
        flower_ids = self.cart.keys()
        flowers = Flower.objects.filter(id__in=flower_ids)
        for flower in flowers:
            self.cart[str(flower.id)]['flower'] = flower

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    # Количество товаров
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True










#one_flower add
def add(self, flower):
        flower_id = str(flower.id)
        if flower_id not in self.cart:
            self.cart[flower_id] = {'price': str(flower.price)}
        self.save()