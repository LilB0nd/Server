from django.template import  loader
from django.http import HttpResponse

from .models import Dish, Order


def detail_order(request, order_id):
    order_list = Order.objects.get(Order_ID=order_id)
    template = loader.get_template('P5/detail_order.html')
    dish_of_order = order_list.Dish_list.all()

    #print(order_list.quantity_set.all())
    quantity = order_list.quantity_set.get_queryset()

    for element in quantity:
        print(element.amount)
        print(element.Dish.Dish_Name)
        print(element.Dish.Dish_Price)



    context = {'dish_list': quantity, "order": order_list}

    return HttpResponse(template.render(context, request))


def all_dishes(request):
    dish = Dish.objects.all()
    return HttpResponse(dish)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
