
from django.conf.urls import url

from . import views

app_name = "P5"

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^order/$', views.OrderView.as_view(), name='OrderView'),
    url(r'^order/(?P<pk>.+)/$', views.DetailOrderView.as_view(), name='DetailOrderView'),
    url(r'^dish$', views.DishView.as_view(), name='dishes'),
    url(r'^dish/(?P<pk>.+)/$', views.DetailDishView.as_view(), name='DetailDishView'),
]