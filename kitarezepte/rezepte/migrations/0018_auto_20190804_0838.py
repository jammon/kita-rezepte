# Generated by Django 2.2.2 on 2019-08-04 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0017_auto_20190804_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rezept',
            name='kategorie',
        ),
        migrations.DeleteModel(
            name='RezeptKategorie',
        ),
    ]
