from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order, DishCategory, DishTyp


class OrderView(generic.ListView):
    template_name = 'P5/order/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.order_by('ID')


class DetailOrderView(generic.DetailView):
    template_name = 'P5/order/detail_order.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(ID=self.object.ID)
        quantity = order.quantity_set.get_queryset()

        context['order'] = order
        context['quantity'] = quantity

        return context

def beleg(request):
    bestell = Order.Order_ID
    price = "ToDo"
    dish = "ToDo"
    content:{
        "bestNr" : bestell
    }
#ToDo
"""
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

class DetailDishView(generic.DetailView):
    template_name = 'P5/dish/detail_dish.html'
    context_object_name = 'dish'
    model = Dish


class DishView(generic.ListView):
    template_name = 'P5/dish/dish_list.html'
    context_object_name = 'dish_list'

    def get_queryset(self):
        return Dish.objects.order_by('typ__dish_category')


def index(request):
    return HttpResponse("Yvo  kann absolut nichts")
# Create your views here.

