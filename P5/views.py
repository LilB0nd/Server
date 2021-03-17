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

class DetailDishView(generic.DetailView):
    template_name = 'P5/dish/detail_dish.html'
    context_object_name = 'dish'
    model = Dish


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
    dishes = Dish.objects.all()
    dish_cat = DishCategory.objects.all()
    dish_typ = DishTyp.objects.all()
    list_of_dish_category = ()
    for dish in dishes:
        dish_category_id = dish.typ.dish_category.id
        if dish_category_id in list_of_dish_category:
            pass
        else:
            list_of_dish_category = list_of_dish_category + (dish_category_id,)

    sorted_dishes = {}
    for dish_id in list_of_dish_category:
        prin = Dish.objects.filter(typ__dish_category_id=dish_id)
        sorted_dishes[id] = prin

    print(sorted_dishes)
    template = loader.get_template('P5/order/templates/P5/dish/dishes.html')
    context = {'dish_list': dishes, 'dish_cat': dish_cat, 'dish_typ': dish_typ, 'sorted_dishes': sorted_dishes}
    return HttpResponse(template.render(context, request))


def index(request):
    return HttpResponse("Yvo kann absolut nichts")
# Create your views here.

