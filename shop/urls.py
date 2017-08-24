from django.conf.urls import url
from . import views
from myshop.settings import MEDIA_ROOT, DEBUG
from django.conf.urls.static import static
from django.conf import settings
from shop.views import FlowerDelete




urlpatterns = [

    url(r'^$', views.main_page, name='main'),
    url(r'^pro_mene/', views.about_me, name='about'),
    url(r'^kontakty', views.contacts, name='contacts'),
    #url(r'^koshyk', views.basket, name='basket'),
    url(r'^basket', views.basket, name='basket'),
    url(r'^samovlenya', views.orders, name='orders'),

    url(r'^flower/(?P<pk>\d+)/one/', views.one_flower, name='one_flower'),

    url(r'^kupyty/', views.main_page, name='buy'),
    url(r'^oformlenya_zamovlenya/', views.OrderCreate, name='OrderCreate'),

    url(r'^dodaty_kvitku', views.flower_add, name='flower_add'),
    url(r'^redahuvaty/(?P<pk>\d+)/kvitku', views.flower_edit, name='flower_edit'),
    url(r'^vydalyty/(?P<pk>\d+)/kvitku', FlowerDelete.as_view(), name='flower_del'),

    url(r'^order/(?P<pk>\d+)/one/', views.one_order, name='one_order'),
    url(r'^add/(?P<flower_id>\d+)/$', views.CartAdd, name='CartAdd'),
    url(r'^ad/(?P<flower_id>\d+)/$', views.CartAdd_basket, name='CartAdd_basket'),
    url(r'^remove/(?P<flower_id>\d+)/$', views.CartRemove, name='CartRemove'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

