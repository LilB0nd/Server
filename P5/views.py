from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order


class OrderView(generic.ListView):
    template_name = 'P5/order/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        print("TEST")
        return Order.objects.order_by('Order_ID')

def detail_order(request, order_id):
    order_list = Order.objects.get(Order_ID=order_id)
    template = loader.get_template('P5/order/detail_order.html')
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
    return HttpResponse("Yvo kann nichts")
# Create your views here.
