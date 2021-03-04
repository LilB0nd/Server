from django.db import models
from djmoney.models.fields import MoneyField
# Models

class Dish(models.Model):
    Appetizer = "Appetizer"
    Main_Dish = "Main Dish"
    Dessert = "Dessert"

    Choices_In_DishTyp = [(Appetizer, "Vorspeise"),
                          (Main_Dish, "Hauptgericht"),
                          (Dessert, "Nachspeise"),]

    Dish_ID = models.AutoField(primary_key=True)
    Dish_Typ = models.CharField(max_length=99, choices=Choices_In_DishTyp, default=Main_Dish)
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
    Dish_list = models.ManyToManyField(Dish)

    def __str__(self):
        return "Bestellung " + str(self.Order_ID)