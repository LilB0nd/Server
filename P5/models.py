from django.core.exceptions import ValidationError
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone
# Models


class DishCategory(models.Model):
    category_name = models.CharField(max_length=99, verbose_name='Gerichtskategorie', default='Allgemein')
    sequence = models.IntegerField(verbose_name='Reihenfolgen', default=3)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name = 'Gerichtskategorie'
        verbose_name_plural = 'Gerichtskategorien'


class DishTyp(models.Model):
    typ_name = models.CharField(max_length=99, verbose_name='Gerichtsvariate', default='Allgemein')
    dish_category = models.ForeignKey(DishCategory, on_delete=models.PROTECT, verbose_name='Gerichtskategorie')

    def __str__(self):
        return self.typ_name

    class Meta:
        verbose_name = 'Gerichtsvariate'
        verbose_name_plural = 'Gerichtsvariaten'


class Dish(models.Model):
    ID = models.AutoField(primary_key=True)
    typ = models.ForeignKey(DishTyp, on_delete=models.PROTECT)
    name = models.CharField(max_length=99)
    description = models.TextField(max_length=512, blank=True)
    currency = (('EUR', 'EURO/€'),)
    price = MoneyField(max_digits=9, decimal_places=2, default_currency='EUR', currency_choices=currency)
    image = models.ImageField()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Gericht'
        verbose_name_plural = 'Gerichte'


class Order(models.Model):
    dish_list = models.ManyToManyField(Dish, through='P5.OrderDetail')
    table_id = models.IntegerField(primary_key=True, unique=True)
    choice = (('open', 'offen'), ('working', 'im Gange'), ('closed', 'abgeschlossen'))
    status = models.CharField(choices=choice, max_length=30, default='open')
    confirmation = models.BooleanField(default=False)
    old_status = None

    def save(self, *args, **kwargs):
        # wird ausgelöst sobald eine Bestellung gespeichert wird, dabei egal ob erstellt oder geändert
        super(Order, self).save(*args, **kwargs)
        if self.pk:
            order = self
            if order.status == 'closed':  # Prüft ob der Status der Bestellung auf abgeschlossen gestellt würde

                new_bill = Bill()
                try:
                    bill_id = Bill.objects.get_queryset().last().ID + 1  # nimmt sich die Bill ID der eben erstellen
                except AttributeError:  # falls es zum Fehler kommt, heißt das, dass es die erste Rechnung war
                    bill_id = 1
                new_bill.ID = bill_id
                new_bill.table_nr = order.table_id
                new_bill.date = timezone.now()

                total_price = self.calucalte_price(OrderDetail.objects.filter(Order__table_id=new_bill.table_nr))
                new_bill.total_price = total_price
                new_bill.given = 0
                new_bill.save()
                for dish in OrderDetail.objects.filter(Order__table_id=new_bill.table_nr):
                    BillDetail.objects.create(Bill=new_bill, Dish=dish.Dish, amount=dish.amount)

                new_bill.save()
                order.delete()
            else:
                super().save()

    @staticmethod
    def calucalte_price(dish_list):  # errechnet den Gesamtpreis der Bestellung
        totalprice = 0
        for dish in dish_list:
            totalprice = totalprice + (dish.Dish.price * dish.amount)

        return totalprice

    def __str__(self):
        return 'Tisch ' + str(self.table_id)

    class Meta:
        verbose_name = 'offene Bestellung'
        verbose_name_plural = 'offene Bestellungen'


class OrderDetail(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Bestellung')
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Gericht')
    amount = models.IntegerField(verbose_name='Anzahl')
    comment = models.CharField(max_length=300, default=None, null=True, blank=True)

    def __str__(self):
        return 'Bestellung ' + str(self.Order.table_id) + ' / ' + str(self.Dish.name)

    class Meta:
        verbose_name = 'Bestellungsdetail'


class Bill(models.Model):
    ID = models.AutoField(primary_key=True, verbose_name='Rechnungsnummer')
    table_nr = models.IntegerField(verbose_name='Tischnummer',)
    dish_list = models.ManyToManyField(Dish, through='P5.BillDetail')
    date = models.DateField(default=timezone.now)

    currency = (('EUR', 'EURO €'),)
    total_price = MoneyField(max_digits=9, decimal_places=2, default_currency='EUR', currency_choices=currency,
                             verbose_name='Gesamtsumme')
    given = MoneyField(max_digits=9, decimal_places=2, default_currency='EUR', currency_choices=currency,
                       verbose_name='Übergeben', blank=True, null=True)
    change = MoneyField(max_digits=9, decimal_places=2, default_currency='EUR', currency_choices=currency,
                        verbose_name='Rückgeld', null=True, blank=True)

    @staticmethod
    def save_statistic(dish, amount):
        try:  # Falls es noch keine Statisktik für das Gericht gibt
            dish_stats = Sales.objects.get(Dish=dish)
            dish_amount = dish_stats.amount
            dish_stats.amount = dish_amount + amount
            dish_stats.save()

        except Sales.DoesNotExist:
            new_dish_stat = Sales()
            new_dish_stat.Dish = dish
            new_dish_stat.amount = amount
            new_dish_stat.save()

    def save(self, *args, **kwargs):
        # wird ausgelöst sobald eine Rechnung gespeichert wird, dabei egal ob erstellt oder geändert
        for dish in BillDetail.objects.filter(Bill=self):  # fügt jedes Gericht der Rechnung der Statistik hinzu
            self.save_statistic(dish.Dish, dish.amount)
        if self.pk:
            if self.given != 0:  # Sobald ein Wert eingegeben wird für den übergebenen Geldbetrag
                change = self.given - self.total_price  # errechnet den Rückgabewert
                if self.given >= self.total_price:
                    # falls given kleiner ist als die Summe wird eine Fehlermeldung in der Methode c0lean hervorgerufen
                    self.change = change
            super(Bill, self).save(*args, **kwargs)

    def clean(self):
        if self.given < self.total_price:
            raise ValidationError({'given': 'Der übergebene Geldbetrag reicht nicht aus'})

    def __str__(self):
        return 'Rechnung ' + str(self.ID)

    class Meta:
        verbose_name = 'Rechnung'
        verbose_name_plural = 'Rechnungen'


class BillDetail(models.Model):
    Bill = models.ForeignKey(Bill, on_delete=models.CASCADE, verbose_name='Bestellung')
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Gericht')
    amount = models.IntegerField(verbose_name='Anzahl')

    def __str__(self):
        return 'Rechnung ' + str(self.Bill.ID) + ' / ' + str(self.Dish.name)


class Sales(models.Model):
    Dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return self.Dish.name

    class Meta:
        verbose_name = 'Verkaufe/Statistik'
        verbose_name_plural = 'Verkaufe/Statistik'
        ordering = ['amount']
