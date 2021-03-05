from django.contrib import admin
from .models import Dish, Order, DishTyp, DishCategory, Quantity

class OrderAdmin(admin.ModelAdmin):
    model = Order
    filter_horizontal = ('Gericht',)

admin.site.register(Quantity)
admin.site.register(Dish)
admin.site.register(DishTyp)
admin.site.register(DishCategory)
admin.site.register(Order)



# Register your models here.
