from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order, DishCategory, DishTyp


class OrderView(generic.ListView):
    template_name = 'P5/order/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.order_by('Order_ID')


class DetailOrderView(generic.DetailView):
    template_name = 'P5/order/detail_order.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(Order_ID=self.object.Order_ID)

        print(order)
        print(order.Table_Nr)
        quantity = order.quantity_set.get_queryset()
        print(quantity)

        context['order'] = order
        context['quantity'] = order.quantity_set.get_queryset()

        return context



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



    context = {'dish_list': quantity, "order": order_list}

    return HttpResponse(template.render(context, request))
"""

def all_dishes(request):
    dish = Dish.objects.all()
    dish_cat = DishCategory.objects.all()
    dish_typ = DishTyp.objects.all()
    template = loader.get_template('P5/dishes.html')
    context = {'dish_list': dish, 'dish_cat': dish_cat, 'dish_typ': dish_typ}
    return HttpResponse(template.render(context, request))


def index(request):
    return HttpResponse("Yvo kann nichts")
# Create your views here.
