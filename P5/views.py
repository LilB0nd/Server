from django.template import  loader
from django.http import HttpResponse

from .models import Dish, Order


def detail_order(request, order_id):
    order_list = Order.objects.get(Order_ID=order_id)
    template = loader.get_template('P5/detail_order.html')
    dish_of_order = order_list.Dish_list.all()
    #print("")
    #print(order_list)
    #print(dish_of_order)
    print("")
    #print(order_list.quantity_set.all())
    quantity = order_list.quantity_set.get_queryset()
    for element in quantity:
        print(element.Dish.Dish_Name)
    print(quantity.Dish.Dish_Name)
    print("")
    context = {'detail_order': order_list, 'dish_list': dish_of_order}
    """
    dishes = ""
    for dish in dish_of_order:
        print(dish)
        dishes = dishes + " " + str(dish)
    
    """
    print(order_list.Dish_list.all())

    return HttpResponse(template.render(context, request))


def all_dishes(request):
    dish = Dish.objects.all()
    return HttpResponse(dish)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
