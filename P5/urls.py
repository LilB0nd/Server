
from django.conf.urls import url

from . import views
app_name = "P5"

urlpatterns = [url('^$', views.index, name='index'),
               url(r'^staffsite/order/$', views.OrderView.as_view(), name='OrderView'),
               url(r'^staffsite/order/(?P<pk>.+)/$', views.DetailOrderView.as_view(), name='DetailOrderView'),
               url(r'^Speisekarte/$', views.DishView.as_view(), name='dishes'),
               url(r'^cart/$', views.DishView.as_view(), name='dishes'),
               url(r'^dish/(?P<pk>.+)/$', views.DetailDishView.as_view(), name='DetailDishView'),
               url(r'dishtest/', views.DishViewTEST.as_view(), name='test'),
               url(r'^staffsite/belege/$', views.beleg, name='beleg'),
               url(r'^staffsite/statistics/$', views.SalesStatisticsView.as_view(), name='SalesView')
               ]

