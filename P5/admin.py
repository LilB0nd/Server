from django.contrib import admin
from .models import *


class BillDetailAdmin(admin.TabularInline):
    model = BillDetail
    extra = 0

    def bill_detail(self, obj):
        return obj.name

    BillDetail.short_description = 'Rechnungdetails'

class BillAdmin(admin.ModelAdmin):
    inlines = [BillDetailAdmin,]

    def bill(self, obj):
        return obj.name

    Bill.short_description = 'Rechnung'

class OrderDetailAdmin(admin.TabularInline):
    list_display = ('Order', 'Dish', 'amount')
    model = OrderDetail
    extra = 0

    def order_detail(self, obj):
        return obj.name

    Order.short_description = 'Bestellungdetails'


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailAdmin, ]

    def order(self, obj):
        return obj

    Order.short_description = 'offene Bestellungen'


class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'typ')

    def dish(self, obj):
        return obj.name

    Dish.short_description = 'Gericht'


class DishTypAdmin(admin.TabularInline):
    list_display = ('typ_name',)
    model = DishTyp
    extra = 0

    def typ(self, obj):
        return obj

    DishTyp.short_description = 'Gerichtsvariante'


class DishCategoryAdmin(admin.ModelAdmin):
    inlines = [DishTypAdmin, ]

    def category(self, obj):
        return obj

    DishCategory.short_description = 'Gerichtskategorie'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)

admin.site.register(Bill)
admin.site.register(BillDetail)

admin.site.register(DishTyp)
admin.site.register(Dish, DishAdmin)
admin.site.register(DishCategory, DishCategoryAdmin)

admin.site.register(Sales)

