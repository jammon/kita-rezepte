# Generated by Django 2.2.4 on 2019-09-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0020_auto_20190912_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gangplan',
            name='gang',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='rezept',
            name='titel',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='rezeptzutat',
            name='menge_qualitativ',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
