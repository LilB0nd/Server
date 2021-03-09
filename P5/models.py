from django.db import models
from djmoney.models.fields import MoneyField
# Models


class DishCategory(models.Model):
    DishCategory_name = models.CharField(max_length=99)

    def __str__(self):
        return str(self.DishCategory_name)

    class Meta:
        verbose_name = "Gerichtsvariate"
        verbose_name_plural = "Gerichtsvariaten"


class DishTyp(models.Model):
    DishTyp_name = models.CharField(max_length=99)
    Dish_Category = models.ForeignKey(DishCategory, on_delete=models.SET_NULL, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.DishTyp_name + " / " + self.Dish_Category.DishCategory_name)

    class Meta:
        verbose_name = "Gerichtskategorie"
        verbose_name_plural = "Gerichtskategorien"


class Dish(models.Model):
    Dish_ID = models.AutoField(primary_key=True)
    Dish_Typ = models.ForeignKey(DishTyp, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    Dish_Name = models.CharField(max_length=99)
    Dish_Description = models.TextField(max_length=512, blank=True)
    Dish_Price = MoneyField(max_digits=9, decimal_places=2, default_currency="EUR")

    def __str__(self):
        return str(self.Dish_Name)

    class Meta:
        verbose_name = "Gericht"
        verbose_name_plural = "Gerichte"
# Create your models here.


class Order(models.Model):
    Order_ID = models.AutoField(primary_key=True)
    Dish_list = models.ManyToManyField(Dish, through='Quantity')
    table_nr_choice = [("table_1", "Tisch 1"), ('table_2', "Tisch 2"), ('table_3', "Tisch 3")]
    Table_Nr = models.CharField(choices=table_nr_choice, max_length=10, default=None)


    def __str__(self):
        return "Bestellung " + str(self.Order_ID)

    class Meta:
        verbose_name = "Bestellung"
        verbose_name_plural = "Bestellungen"


class Quantity(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return "Bestellung " + str(self.Order.Order_ID) + "/ Gericht " + str(self.Dish) + " / Anzahl " + str(self.amount)