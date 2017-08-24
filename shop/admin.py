# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Flower
from .models import Order, OrderItem



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']



class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']
    inlines = [OrderItemInline]


admin.site.register(Flower)
admin.site.register(Order, OrderAdmin)


