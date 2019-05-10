from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='fresh'),
    path('fresh/<int:p>', views.index, name='fresh'),
    path('freshs/', views.indexs, name='freshs'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('info/', views.info, name='info'),
    # path('about_index/', views.about_index, name='about_index'),
    path('shopping/<int:p>', views.shoppings, name='shoppings'),
    path('shopping/', views.shopping, name='shopping'),
    path('shop/<int:p>', views.shop, name='shop'),
    path('order/', views.order, name='order'),
    path('site/', views.site, name='site'),
    path('cart/', views.cart, name='cart'),
    path('detail/<int:detail_id>', views.detail, name='detail'),
    path('dizhi/', views.dizhi, name='dizhi'),
    path('adds/', views.adds, name='adds'),
    path('list/<int:list_id><int:p>', views.list, name='list_fenye'),
    path('list/<int:list_id>', views.list, name='list'),
    path('shanchu/<int:shop_id>', views.shanchu, name='shanchu'),
    path('place_order/', views.place_order, name='place_order')
]