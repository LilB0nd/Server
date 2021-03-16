from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('P5/', include('P5.urls')),
    path('admin/', admin.site.urls),
]