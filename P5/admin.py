from django.contrib import admin
from .models import Dish, Order

class OrderAdmin(admin.ModelAdmin):
    model = Order
    filter_horizontal = ('Gericht',)

admin.site.register(Dish)
admin.site.register(Order)


# Register your models here.
