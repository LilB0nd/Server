
from django.conf.urls import url

from . import views

app_name = "P5"

urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^order/$', views.OrderView.as_view(), name='OrderView'),
    url(r'^order/(?P<order_id>.+)/$', views.detail_order, name='detail_order'),
]