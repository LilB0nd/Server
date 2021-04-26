from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order, DishCategory, DishTyp, OrderDetail, Sales


class OrderView(generic.ListView):
    template_name = 'P5/staffsite/order/order_list.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.order_by('ID')


class DetailOrderView(generic.DetailView):
    template_name = 'P5/staffsite/order/detail_order.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(ID=self.object.ID)
        quantity = order.orderdetail_set.get_queryset()

        context['order'] = order
        context['quantity'] = quantity

        return context


all_order_list = [('Suppe',3,10),('Suppe',3,10),('Suppe',3,10),('Suppe',3,10),('Suppe',3,10),('Suppe',3,10)]
def rechner (all_order_list:list)-> float:

    price = 0

    for item in all_order_list:

        price += item[1]*item[2]

    return price

def beleg(request):

    zwisch = rechner(all_order_list)
    Mwst_not_rounded = (zwisch * 0.19)
    Mwst = round(Mwst_not_rounded, 2)
    gsmt_not_rounded = (zwisch + Mwst)
    gmst = round(gsmt_not_rounded, 2)
    content = {
        'all_orders_list' : all_order_list,
        'zwischen' : zwisch,
        'mehrwert': Mwst,
        'gesamt': gmst
    }
    return render(request, "P5/Rechnungen/belege.html", content)


class DetailDishView(generic.DetailView):
    template_name = 'P5/dish/detail_dish.html'
    context_object_name = 'dish'
    model = Dish



class DishView(generic.ListView):
    template_name = 'P5/dish/dish_list.html'
    context_object_name = 'dish_list'
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_id = self.request.GET.get('table_id')
        print(table_id)
        list_category = []
        list_typ = DishTyp.objects.all()
        dish_list = Dish.objects.order_by('typ__dish_category')

        for category in dish_list:
            if category.typ.dish_category in list_category:
                pass
            else:
                list_category.append(category.typ.dish_category)


        context['list_typ'] = list_typ
        context['dish_list'] = dish_list
        context['list_category'] = list_category

        return context

class CartView(generic.ListView):
    template_name = 'P5/dish/cart.html'
    context_object_name = 'order'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order_id = self.request.GET.get('order_id')
        order = Order.objects.get(ID=order_id)
        quantity = order.orderdetail_set.get_queryset()
        print('TEST')
        context['quantity'] = quantity
        context['order'] = order

        return context


class DishViewTEST(generic.ListView):
    template_name = 'P5/dish/test.html'
    context_object_name = 'dish_list'
    model = Dish

    def post(self, request, *args, **kwargs):
        self.create_new_order()
        self.set_dishes_for_order()
        return redirect('P5:DetailOrderView', pk=self.new_order.id)

    def create_new_order(self):
        self.new_order = Order()
        self.new_order.table_nr = 1
        try:
            last_order_id = Order.objects.last().ID
            self.new_order.id = last_order_id + 1
        except AttributeError:
            self.new_order.id = 1
        self.new_order.save()

    def set_dishes_for_order(self):
        for dish in Dish.objects.all():
            dish_id = dish.ID
            amount = int(self.request.POST[str(dish.ID) + ':amount'])
            print(amount)
            if amount != 0:
                print('SAVe')
                new_quantity = OrderDetail()
                self.save_statistic(dish, amount)
                new_quantity.Order = Order.objects.get(ID=self.new_order.id)
                new_quantity.Dish = Dish.objects.get(ID=dish_id)
                new_quantity.amount = amount
                new_quantity.save()

    def save_statistic(self, dish, amount):
        try:
            dish_stats = Sales.objects.get(Dish=dish)
            dish_amount = dish_stats.amount
            dish_stats.amount = dish_amount + dish_amount
            dish_stats.save()

        except Sales.DoesNotExist:
            new_dish_stat = Sales()
            new_dish_stat.Dish = dish
            new_dish_stat.amount = amount
            new_dish_stat.save()



class SalesStatisticsView(generic.ListView):
    template_name = 'P5/staffsite/Sales/all_stats.html'
    context_object_name = 'stats'
    model = Sales



def index(request):
    return HttpResponse('<a href="/P5/staffsite/order/"> Bestellungen</a><a href="/P5/dishtest/"> Gerichte bestellen</a><a href="/P5/staffsite/statistics/"> Statistics</a>')
