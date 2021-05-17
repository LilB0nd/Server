# Generated by Django 3.0.5 on 2021-05-07 10:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False, verbose_name='Rechnungsnummer')),
                ('table_nr', models.IntegerField(verbose_name='Tischnummer')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('total_price_brutto_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EURO €')], default='EUR', editable=False, max_length=3)),
                ('total_price_brutto', djmoney.models.fields.MoneyField(currency_choices=(('EUR', 'EURO €'),), decimal_places=2, default_currency='EUR', max_digits=9, verbose_name='Gesamtsumme')),
                ('given_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EURO €')], default='EUR', editable=False, max_length=3)),
                ('given', djmoney.models.fields.MoneyField(currency_choices=(('EUR', 'EURO €'),), decimal_places=2, default_currency='EUR', max_digits=9, verbose_name='Übergeben')),
                ('tip_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EURO €')], default='EUR', editable=False, max_length=3)),
                ('tip', djmoney.models.fields.MoneyField(blank=True, currency_choices=(('EUR', 'EURO €'),), decimal_places=2, default_currency='EUR', max_digits=9, null=True, verbose_name='Trinkgeld')),
                ('change_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EURO €')], default='EUR', editable=False, max_length=3)),
                ('change', djmoney.models.fields.MoneyField(currency_choices=(('EUR', 'EURO €'),), decimal_places=2, default_currency='EUR', max_digits=9, verbose_name='Trinkgeld')),
            ],
            options={
                'verbose_name': 'Rechnung',
                'verbose_name_plural': 'Rechnungen',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=99)),
                ('description', models.TextField(blank=True, max_length=512)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'EURO/€')], default='EUR', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(currency_choices=(('EUR', 'EURO/€'),), decimal_places=2, default_currency='EUR', max_digits=9)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Gericht',
                'verbose_name_plural': 'Gerichte',
            },
        ),
        migrations.CreateModel(
            name='DishCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=99, verbose_name='Gerichtskategorie')),
                ('sequence', models.IntegerField(default=3, verbose_name='Reihenfolgen')),
            ],
            options={
                'verbose_name': 'Gerichtskategorie',
                'verbose_name_plural': 'Gerichtskategorien',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('table_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('open', 'offen'), ('working', 'im Gange'), ('closed', 'abgeschlossen')], default='open', max_length=30)),
                ('confirmation', models.BooleanField(default=False)),
                ('comment', models.CharField(default=None, max_length=300)),
            ],
            options={
                'verbose_name': 'offene Bestellung',
                'verbose_name_plural': 'offene Bestellungen',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('Dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P5.Dish')),
            ],
            options={
                'verbose_name': 'Verkaufe/Statistik',
                'verbose_name_plural': 'Verkaufe/Statistik',
                'ordering': ['amount'],
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Anzahl')),
                ('Dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P5.Dish', verbose_name='Gericht')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P5.Order', verbose_name='Bestellung')),
            ],
            options={
                'verbose_name': 'Bestellungsdetail',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='dish_list',
            field=models.ManyToManyField(through='P5.OrderDetail', to='P5.Dish'),
        ),
        migrations.CreateModel(
            name='DishTyp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ_name', models.CharField(max_length=99, verbose_name='Gerichtsvariate')),
                ('dish_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='P5.DishCategory', verbose_name='Gerichtskategorie')),
            ],
            options={
                'verbose_name': 'Gerichtsvariate',
                'verbose_name_plural': 'Gerichtsvariaten',
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='typ',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='P5.DishTyp'),
        ),
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Anzahl')),
                ('Bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P5.Bill', verbose_name='Bestellung')),
                ('Dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='P5.Dish', verbose_name='Gericht')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='dish_list',
            field=models.ManyToManyField(through='P5.BillDetail', to='P5.Dish'),
        ),
    ]