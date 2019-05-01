# Generated by Django 2.1.7 on 2019-05-01 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0013_auto_20190414_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rezept',
            name='ist_hauptgang',
        ),
        migrations.RemoveField(
            model_name='rezept',
            name='ist_nachtisch',
        ),
        migrations.RemoveField(
            model_name='rezept',
            name='ist_vorspeise',
        ),
        migrations.AlterField(
            model_name='zutat',
            name='einheit',
            field=models.CharField(blank=True, default='', help_text='Packungseinheit für den Einkauf meist 1 kg, 1 l,\n             aber auch 2,5 kg-Sack.\n             Fällt weg bei Dingen wie Eiern, die eine natürliche Einheit\n             haben; dann "Stück"', max_length=10),
        ),
        migrations.AlterField(
            model_name='zutat',
            name='menge_pro_einheit',
            field=models.IntegerField(default=0, help_text='Anzahl der Masseinheiten pro Packungseinheit; bei 1 kg: 1000'),
        ),
    ]
