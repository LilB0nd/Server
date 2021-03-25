from django.contrib import admin
from .models import *
"""
class OrderAdmin(admin.ModelAdmin):
    model = Order
    filter_horizontal = ('Gericht',)
"""
admin.site.register(OrderDetail)
admin.site.register(Dish)
admin.site.register(DishTyp)
admin.site.register(DishCategory)
admin.site.register(Order)




# Register your models here.
