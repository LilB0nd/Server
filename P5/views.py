from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order, DishCategory, DishTyp, OrderDetail, Sales

class Bill:

    def rechner (self, all_order_list: list)-> float:

        price = 0

        for item in all_order_list:

            price += item[1]*item[2]

        return price

    def beleg(self, request, all_order_list, table_id):

        zwisch = self.rechner(all_order_list)
        Mwst_not_rounded = (zwisch * 0.19)
        Mwst = round(Mwst_not_rounded, 2)
        gsmt_not_rounded = (zwisch + Mwst)
        gmst = round(gsmt_not_rounded, 2)

        content = {
            'all_orders_list': all_order_list,
            'zwischen': zwisch,
            'mehrwert': Mwst,
            'gesamt': gmst,
            'table': table_id
        }
        return render(request, "P5/Rechnungen/belege.html", content)


class DishView(generic.ListView):
    template_name = 'P5/dish/dish_list.html'
    context_object_name = 'dish_list'
    model = Dish

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_id = self.request.GET.get('table_id')
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
        context['table_id'] = table_id
        print(table_id)

        self.create_new_order()

        return context

    def create_new_order(self):
        self.new_order = Order()
        table_id = int(self.request.GET.get('table_id'))  # table number out of url
        self.new_order.table_id = table_id  # set table number as new_order id
        self.new_order.save()  # save new order

    def post(self, *args, **kwargs):
        self.table_id = int(self.request.GET.get('table_id'))
        self.set_dishes_for_order()
        respone = HttpResponse()
        respone.status_code = 204
        return respone

    def set_dishes_for_order(self):
        order = Order.objects.get(table_id=self.table_id)
        dish_id = int(self.request.POST['dish_name'])
        comment = self.request.POST['info']
        dish_list = order.orderdetail_set.all()

        try:
            order_dish = dish_list.get(Order_id=self.table_id, Dish_id=dish_id)
            order_dish.amount = order_dish.amount + 1
            order_dish.comment = order_dish.comment + '\n' + comment
            order_dish.save()

        except Dish.DoesNotExist and OrderDetail.DoesNotExist:
            new_dish_to_order = OrderDetail()
            new_dish_to_order.Order = Order.objects.get(table_id=self.table_id)
            new_dish_to_order.Dish = Dish.objects.get(ID=dish_id)
            new_dish_to_order.amount = 1
            new_dish_to_order.comment = comment
            new_dish_to_order.save()

    def save_statistic(self, dish, amount):
        try:
            dish_stats = Sales.objects.get(Dish=dish)
            dish_amount = dish_stats.amount
            dish_stats.amount = dish_amount + amount
            dish_stats.save()

        except Sales.DoesNotExist:
            new_dish_stat = Sales()
            new_dish_stat.Dish = dish
            new_dish_stat.amount = amount
            new_dish_stat.save()

class CartView(generic.ListView):
    template_name = 'P5/dish/cart.html'
    context_object_name = 'order'
    model = Order


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.order_id = self.kwargs.get('order_id')
        order = Order.objects.get(table_id=self.order_id)
        quantity = order.orderdetail_set.get_queryset()
        full_price = self.get_price()[0]
        order_details = self.get_price()[1]

        context['order'] = order
        context['quantity'] = quantity
        context['full_price'] = full_price
        context['order_details'] = order_details

        return context

    def get_price(self):
        bestellung = [0, []]
        order = Order.objects.get(table_id=self.order_id)
        quantity = order.orderdetail_set.get_queryset()

        for dish in quantity:
            if dish.amount == 0:
                pass
            else:
                fullprice = dish.amount * dish.Dish.price

                order_list = [str(dish.amount), dish.Dish.name, str(fullprice), dish.comment]
                bestellung[0] = bestellung[0] + fullprice
                bestellung[1].append(order_list)
                print(bestellung[1])

        return bestellung

    def post(self, request,  *args, **kwargs):

        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(table_id=order_id)

        if "remove" in self.request.POST:
            name = str(self.request.POST['remove'])
            self.remove(name, order)
            return redirect('/P5/cart/' + str(order_id) + '/')

        elif "order" in self.request.POST:
            order.confirmation = True
            order.status = "working"
            order.save()
            return redirect('/P5/cart/' + str(order_id) + '/')

        elif "pay" in self.request.POST:

            return render(request, "P5/Rechnungen/mail_input.html")

        elif "finish" in self.request.POST:

            print("hi")

            return render(request, "P5/Rechnungen/end.html")

    def remove(self, name, order):

        quantity = order.orderdetail_set.get_queryset()

        for dish in quantity:
            if name == dish.Dish.name:
                print(name)
                dish.amount = dish.amount - 1
                dish.save()

        return




def index(request):
    return HttpResponse('<a href="/P5/staffsite/order/"> Bestellungen</a><a href="/P5/dishtest/"> Gerichte bestellen</a><a href="/P5/staffsite/statistics/"> Statistics</a>')
