from django.db import models
from djmoney.models.fields import MoneyField
from datetime import datetime
# Models


class DishCategory(models.Model):
    category_name = models.CharField(max_length=99)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Gerichtskategorie'
        verbose_name_plural = 'Gerichtskategorien'


class DishTyp(models.Model):
    typ_name = models.CharField(max_length=99)
    dish_category = models.ForeignKey(DishCategory, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.dish_category.category_name + ' / ' + self.typ_name)

    class Meta:
        verbose_name = 'Gerichtsvariate'
        verbose_name_plural = 'Gerichtsvariaten'


class Dish(models.Model):
    ID = models.AutoField(primary_key=True)
    typ = models.ForeignKey(DishTyp, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    name = models.CharField(max_length=99)
    description = models.TextField(max_length=512, blank=True)
    price = MoneyField(max_digits=9, decimal_places=2, default_currency='EUR')
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Gericht'
        verbose_name_plural = 'Gerichte'
# Create your models here.


class Order(models.Model):
    ID = models.AutoField(primary_key=True)
    dish_list = models.ManyToManyField(Dish, through='P5.OrderDetail')
    date = models.DateField(default=datetime.now())
    table_nr = models.IntegerField()

    def __str__(self):
        return 'Bestellung ' + str(self.ID)

    class Meta:
        verbose_name = 'Bestellung'
        verbose_name_plural = 'Bestellungen'


class OrderDetail(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return 'Bestellung ' + str(self.Order.ID) + '/ ' + str(self.amount) + 'x ' + str(self.Dish)


class Sales(models.Model):
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()

