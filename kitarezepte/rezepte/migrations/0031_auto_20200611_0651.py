# Generated by Django 3.0.6 on 2020-06-11 04:51

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0030_auto_20200607_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezept',
            name='_preis',
            field=models.DecimalField(decimal_places=2, default=Decimal('-1'), help_text='kann leer sein, wird dann automatisch berechnet', max_digits=5),
        ),
    ]
