from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views

app_name = "P5"

urlpatterns = [url('^$', views.index, name='index'),

            url(r'^Speisekarte/$', views.DishView.as_view(), name='dishes'),
            url(r'^cart/(?P<order_id>.+)/$', views.CartView.as_view(), name='Cart'),
            url(r'^Beleg', views.BelegView.as_view(), name='Beleg'),
            url(r'^MailInput/', views.MailInput.as_view(), name='Mail'),
            url(r'^Finish/', views.Finish.as_view(), name='Finish'),

            url(r'^staffsite/belege/$', login_required(views.Bill_view.beleg), name='beleg')]

