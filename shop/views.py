# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Flower
from .models import Order, OrderItem
from .util import basket_list
from .util import flow_count_name
from .util import suma
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.forms import ModelForm
from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from time import time
from .util import is_digit
from datetime import datetime
from .cart import Cart
from .forms import CartAddProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger







###########################################################################
def main_page(request):
  cart = Cart(request)
  flowers = Flower.objects.all()
  fl_count = flow_count_name(request)
  count = len(Cart(request))
  #pagination
  paginator = Paginator(flowers, 4)
  page = request.GET.get('page')
  try:
    flowers = paginator.page(page)
  except PageNotAnInteger:
    flowers = paginator.page(1)
  except EmptyPage:
    flowers= paginator.page(paginator.num_pages)
  return render(request, 'shop/main.html', {'flowers':flowers, 'count': count,
     'fl_count': fl_count, 'count': count, 'cart': cart})
  





def CartAdd(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    cart.add(flower=flower, quantity=1)
    return redirect('main')




def CartAdd_basket(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(flower=flower, quantity=cd['quantity'],
                                  update_quantity=cd['update'])
    return redirect('basket')





def CartRemove(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    cart.remove(flower)
    return redirect('basket')






def basket(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(request, 'shop/basket.html', {'cart': cart})

#####################################################################
def about_me(request):
	return render(request, 'shop/about.html', {})


####################################################################
def contacts(request):
	return render(request, 'shop/contacts.html', {})





################################################################

#order_confirm


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        errors = {}
        data = {}

        # validate user input
        name = request.POST.get('name', '').strip()
        if not name:
          errors['name'] = u"Ім'я є обов'язковим"
        else:
          data['name'] = name

        number = request.POST.get('number', '').strip()
        if not number:
          errors['number'] = u"Номер телефону є обов'язковим"
        else:
          data['number'] = number

        notes = request.POST.get('notes', '').strip()
        if notes:
          data['notes'] = notes
        
        total_cost = request.POST.get('total_cost', '').strip()
        data['total_cost'] = total_cost
        
        if not errors:
          order = Order(**data)
          order.save()
          for item in cart:
            OrderItem.objects.create(order=order, product=item['flower'],
                                         price=item['price'],
                                         quantity=item['quantity'])
          cart.clear()
          return HttpResponseRedirect( u'%s?status_message=Замовлення успішно збережено!' 
              % reverse('main'))
        else:
          return render(request, 'shop/ordering.html',
            {'errors': errors})

    return render(request, 'shop/ordering.html', {'cart': cart})


#####################################################################
def one_flower(request, pk):
  flower = Flower.objects.filter(pk=pk)
  fl_count = flow_count_name(request)
  count = len(basket_list(request))
  return render(request, 'shop/one_flower.html', {'flower':flower, 'count': count, 'fl_count': fl_count})









######################################################################
@login_required
def orders(request):
  orders = Order.objects.all()
  return render(request, 'shop/orders.html', {'orders': orders})




#########################################################################
#flower_add

def flower_add(request):
  # was form posted?
  if request.method == "POST":
    # was form add button clicked?
    if request.POST.get('add_button') is not None:
      # errors collection
      errors = {}
      # data for student object
      data = {}
      # validate user input
      title = request.POST.get('title', '').strip()
      if not title:
        errors['title'] = u"Ім'я є обов'язковим"
      else:
        data['title'] = title

      data['lat_title'] = time()
        
        
      price = request.POST.get('price', '').strip()
      if not price:
          errors['price'] = u"Ціна є обов'язковою"
      else:
          if is_digit(price) == 1:
            data['price'] = price
          else:
            errors['price'] = u"Введіть ціле число!"
      description = request.POST.get('description', '').strip()
      if not description:
        errors['description'] = u"Опис є обов'язковим"
      else:
        data['description'] = description  
      photo_main = request.FILES.get('photo_main')
      if not photo_main:
        errors['photo_main'] = u"Одне фото є обов'язковим"
      else:
        data['photo_main'] = photo_main 
      photo_big = request.FILES.get('photo_big')
      if photo_big:
        data['photo_big'] = photo_big 

           
      # save flovwer
      if not errors:
        flower = Flower(**data)
        flower.save()
        # redirect to students list
        return HttpResponseRedirect( u'%s?status_message=Квітку успішно додано!'  % reverse('main'))
      else:
        # render form with errors and previous user input
        return render(request, 'shop/flower_add.html',
        {'errors': errors})
    elif request.POST.get('cancel_button') is not None:
      # redirect to home page on cancel button
      return HttpResponseRedirect( u'%s?status_message=Додавання квітки скасовано!' % reverse('main'))
  else:
   # initial form render
   return render(request, 'shop/flower_add.html', {})




#####################################################################
#flower_edit


def flower_edit(request, pk):
    flower = Flower.objects.filter(pk=pk)

    
    if request.method == "POST":
        data = Flower.objects.get(pk=pk)
        if request.POST.get('add_button') is not None:
            
            errors = {}

            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Імʼя є обовʼязковим."
            else:
                data.title = title

            data.lat_title = time()

            price = request.POST.get('price', '').strip()
            if not price:
               errors['price'] = u"Ціна є обов'язковою"
            else:
               if is_digit(price) == 1:
                 data.price = price 
               else:
                 errors['price'] = u"Введіть ціле число!"

            description = request.POST.get('description', '').strip()
            if not description:
               errors['description'] = u"Опис є обов'язковим"
            else:
               data.description = description
            photo_main = request.FILES.get('photo_main')
            if not photo_main:
                errors['photo_main'] = u"Одне фото є обов'язковим"
            else:
                data.photo_main = photo_main 
            photo_big = request.FILES.get('photo_big')
            if photo_big:
               data.photo_big = photo_big 


            if errors:
                return render(request, 'shop/flower_edit.html', {'pk': pk, 'flower': data, 'errors': errors})
            else:
                data.save()
                return HttpResponseRedirect(u'%s?status_message=Редагування квітки  завершено' % reverse('main'))
        elif request.POST.get('cancel_button') is not None:

            return HttpResponseRedirect(u'%s?status_message=Редагування квітки скасовано!' % reverse('main'))
        
    else:
        return render(request,
                      'shop/flower_edit.html', {'pk': pk, 'flower': flower[0]})
                      
                      
                    






########################################

#flower delete

class FlowerDelete(DeleteView):
  model = Flower
  template_name = 'shop/flower_delete.html'
  def get_success_url(self):
    return u'%s?status_message=Квітку успішно видалено!' % reverse('main')
  def post(self, request, *args, **kwargs):
    if request.POST.get('no_delete_button'):
      return HttpResponseRedirect(u'%s?status_message=Видалення  квітки відмінено!'% reverse('main'))
    else:
      return super(FlowerDelete, self).post(request, *args, **kwargs)
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
        return super(FlowerDelete, self).dispatch(*args, **kwargs)




###############################################################################

def one_order(request, pk):
  order = Order.objects.get(pk=pk)
  products = OrderItem.objects.filter(order=order)
  return render(request, 'shop/one_order.html', {'order':order, 'products': products})




