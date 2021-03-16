from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order/<int:order_id>', views.detail_order, name='order'),
    path('dishes', views.all_dishes, name='dishes' )
]