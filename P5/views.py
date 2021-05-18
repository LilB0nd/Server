from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Dish, Order, DishCategory, DishTyp, OrderDetail, Sales, Bill
from Quittung import Quittungenfüllen


class Bill_view:

    def rechner (self, all_order_list):

        price = 0

        for item in all_order_list:

            price += item[1]*item[2]

        return price *0.81

    def beleg(self, request, all_order_list, table_id):

        zwisch = self.rechner(all_order_list)
        Mwst_not_rounded = ((zwisch/0.81)*0.19)
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

    def quittung(self, request, all_order_list, table_id):
        zwisch = self.rechner(all_order_list)
        Mwst_not_rounded = ((zwisch / 0.81) * 0.19)
        Mwst = round(Mwst_not_rounded, 2)
        gsmt_not_rounded = (zwisch + Mwst)
        gmst = round(gsmt_not_rounded, 2)
        paid = Bill.given
        change = Bill.change

        content = {
            'all_orders_list': all_order_list,
            'zwischen': zwisch,
            'mehrwert': Mwst,
            'gesamt': gmst,
            'table': table_id,
            'paid': paid,
            'change': change
        }
        return render(request, "P5/Rechnungen/Quittung.html", content)


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
            if order_dish.comment:
                order_dish.comment = order_dish.comment + ', ' + comment
            else:
                order_dish.comment = comment
            order_dish.save()


        except Dish.DoesNotExist and OrderDetail.DoesNotExist:
            new_dish_to_order = OrderDetail()
            new_dish_to_order.Order = Order.objects.get(table_id=self.table_id)
            new_dish_to_order.Dish = Dish.objects.get(ID=dish_id)
            new_dish_to_order.amount = 1
            new_dish_to_order.comment = comment
            new_dish_to_order.save()



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

            #ToDO  Max liste geben
            return redirect('/P5/Beleg/?table_id=' + str(order_id))


    def order_sorter(self, order_id)-> list:
        order = Order.objects.get(table_id=order_id)
        quantity = order.orderdetail_set.get_queryset()

        sorted_order = []

        for i in quantity:

            order_list = (i.Dish.name, i.amount, i.Dish.price)
            if not order_list[1] == 0:
                sorted_order.append(order_list)

        return sorted_order

    def remove(self, name, order):

        quantity = order.orderdetail_set.get_queryset()

        for dish in quantity:
            if name == dish.Dish.name:
                dish.amount = dish.amount - 1
                dish.save()

        return


class BelegView(generic.TemplateView):

    template_name = 'P5/Rechnungen/belege.html'

    def rechner(self, all_order_list: list) -> float:
        price = 0

        for item in all_order_list:
            price += item[1] * item[2]

        return price * 0.81

    def get_context_data(self, **kwargs):

        table_id = self.request.GET.get('table_id')
        all_order_list = self.order_sorter(table_id)
        table_id = Order.objects.get(table_id=table_id)

        zwisch = self.rechner(all_order_list)
        mwst_not_rounded = ((zwisch / 0.81) * 0.19)
        mwst = round(mwst_not_rounded, 2)
        gsmt_not_rounded = (zwisch + mwst)
        gmst = round(gsmt_not_rounded, 2)

        content = {
            'all_orders_list': all_order_list,
            'zwischen': zwisch,
            'mehrwert': mwst,
            'gesamt': gmst,
            'table': table_id
        }
        return content

    def order_sorter(self, order_id)-> list:
        order = Order.objects.get(table_id=order_id)
        quantity = order.orderdetail_set.get_queryset()

        sorted_order = []

        for i in quantity:

            order_list = (i.Dish.name, i.amount, i.Dish.price)
            if not order_list[1] == 0:
                sorted_order.append(order_list)

        return sorted_order

    def post(self, *args, **kwargs):
        order = Order.objects.get(table_id=self.request.GET.get('table_id'))

        if "bill" in self.request.POST:

            order.status = "closed"
            order.save()
            bill_id = (str(Bill.objects.last().ID))

            return redirect('/P5/MailInput/?order_id='+bill_id)


class MailInput(generic.TemplateView):

    template_name = 'P5/Rechnungen/mail_input.html'

    def post(self, request):

        order_id = self.request.GET.get('order_id')
        bill = Bill.objects.get(ID=order_id)

        if "finish" in self.request.POST:

            # ToDo
            '''Anile´s Stuff'''

            if str(bill.given) != "0.00 €":
                Quittungenfüllen.Mail(self.get_email(), "")

                return redirect('/P5/Quittung/?order_id=' + str(self.request.GET.get('order_id')))

            else:
                respone = HttpResponse()
                respone.status_code = 204
                return respone

    def get_email(self):

        mail = self.request.POST['email']

        return mail


class QuittungView(generic.TemplateView):

    template_name = 'P5/Rechnungen/Quittung.html'

    def rechner(self, all_order_list: list) -> float:
        price = 0

        for item in all_order_list:
            price += item[1] * item[2]

        return price * 0.81

    def get_context_data(self, **kwargs):
        order_id = self.request.GET.get('order_id')
        bill = Bill.objects.get(ID=order_id)

        all_order_list = self.order_sorter(bill)


        zwisch = self.rechner(all_order_list)
        mwst_not_rounded = ((zwisch / 0.81) * 0.19)
        mwst = round(mwst_not_rounded, 2)
        gsmt_not_rounded = (zwisch + mwst)
        gmst = round(gsmt_not_rounded, 2)
        bill_id = bill.ID
        paid = bill.given
        change = bill.change
        table_nr = bill.table_nr

        content = {
            'all_orders_list': all_order_list,
            'zwischen': zwisch,
            'mehrwert': mwst,
            'gesamt': gmst,
            'table': table_nr,
            'paid': paid,
            'change': change,
            'ID': bill_id

        }
        print(paid)
        print(change)
        return content

    def order_sorter(self, bill)-> list:
        bill_detail = bill.billdetail_set.get_queryset()

        sorted_order = []

        for i in bill_detail:

            order_list = (i.Dish.name, i.amount, i.Dish.price)
            if not order_list[1] == 0:
                sorted_order.append(order_list)

        return sorted_order


class Finish(generic.TemplateView):
    template_name = 'P5/Rechnungen/end.html'



def index(request):
    return render(request, "P5/Base/Index.html")
####