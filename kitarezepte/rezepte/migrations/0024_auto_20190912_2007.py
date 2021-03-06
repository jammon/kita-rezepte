# Generated by Django 2.2.4 on 2019-09-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0023_auto_20190912_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='kategorien',
            field=models.CharField(blank=True, default='', help_text='z.B. "Reis Teigwaren Getreide Kartoffeln Gemüse Suppe Fischgericht Lieblingsgericht"', max_length=100),
        ),
        migrations.AlterField(
            model_name='rezept',
            name='kategorien',
            field=models.CharField(blank=True, default='', help_text='Die Kategorie, zu der das Rezept gehört, ggf. eine Leerzeichen-getrennte Liste mehrerer Kategorien', max_length=60),
        ),
    ]
