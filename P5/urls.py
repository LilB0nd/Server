from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views

app_name = "P5"

urlpatterns = [url('^$', views.index, name='index'),

               url(r'^Speisekarte/$', views.DishView.as_view(), name='dishes'),
               url(r'^cart/(?P<pk>.+)/$', views.CartView.as_view(), name='Cart'),
               url(r'^dish/(?P<pk>.+)/$', views.DetailDishView.as_view(), name='DetailDishView'),
               #url(r'dishtest/', views.DishViewTEST.as_view(), name='test'),

               # Staffsite
               url(r'^login/$', auth_views.LoginView.as_view(), name='login'),

               url(r'^staffsite/belege/$', login_required(views.beleg), name='beleg'),
               url(r'^staffsite/statistics/$', login_required(views.SalesStatisticsView.as_view()), name='SalesView'),
               url(r'^staffsite/order/$', login_required(views.OrderView.as_view()), name='OrderView'),
               url(r'^staffsite/order/(?P<pk>.+)/$', login_required(views.DetailOrderView.as_view()), name='DetailOrderView'),
               url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
               ]
