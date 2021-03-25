from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import generic, View
from io import BytesIO
from xhtml2pdf import pisa
from .models import Dish, Order, DishCategory, DishTyp


def render_to_pdf(template_src, context_dict: dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        zwisch = rechner(all_order_list)
        Mwst_not_rounded = (zwisch * 0.19)
        Mwst = round(Mwst_not_rounded, 2)
        gsmt_not_rounded = (zwisch + Mwst)
        gmst = round(gsmt_not_rounded, 2)
        content = {
            'all_orders_list': all_order_list,
            'zwischen': zwisch,
            'mehrwert': Mwst,
            'gesamt': gmst
        }

        pdf = render_to_pdf("app/pdf_template", content)
        return HttpResponse(pdf, content_type="application/pdf")


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


all_order_list = [('Suppe', 3, 10), ('Suppe', 3, 10), ('Suppe', 3, 10), ('Suppe', 3, 10), ('Suppe', 3, 10),
                  ('Suppe', 3, 10)]


def rechner(all_order_list: list) -> float:
    price = 0

    for item in all_order_list:
        price += item[1] * item[2]

    return price


def beleg(request):
    zwisch = rechner(all_order_list)
    Mwst_not_rounded = (zwisch * 0.19)
    Mwst = round(Mwst_not_rounded, 2)
    gsmt_not_rounded = (zwisch + Mwst)
    gmst = round(gsmt_not_rounded, 2)
    content = {
        'all_orders_list': all_order_list,
        'zwischen': zwisch,
        'mehrwert': Mwst,
        'gesamt': gmst
    }
    return render(request, "P5/Rechnungen/belege.html", content)


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
"""


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
        list_category = DishCategory.objects.all()
        list_typ = DishTyp.objects.all()
        dish_list = Dish.objects.order_by('typ__dish_category')

        context['list_typ'] = list_typ
        context['dish_list'] = dish_list
        context['list_category'] = list_category

        return context


def index(request):
    return HttpResponse("Yvo kann absolut gar nichts")
# Create your views here.
