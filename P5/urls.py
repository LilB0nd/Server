
from django.conf.urls import url

from . import views

app_name = "P5"

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^order/$', views.OrderView.as_view(), name='OrderView'),
    url(r'^order/(?P<pk>.+)/$', views.DetailOrderView.as_view(), name='DetailOrderView'),
    url(r'^dishes$', views.all_dishes, name='dishes'),
]