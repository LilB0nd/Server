from django.shortcuts import render
from django.http import HttpResponse
from .models import Dish, Order


def detail_order(request, order_id):
    order_list = Order.objects.get(Order_ID=order_id)
    print("")
    print(order_list)
    dish_of_order = order_list.Dish_list.all()
    dishes = ""
    for dish in dish_of_order:
        print(dish)
        dishes = dishes + " " + str(dish)
    print(dish_of_order)
    return HttpResponse(dishes)


def all_dishes(request):
    dish = Dish.objects.all()
    return HttpResponse(dish)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
