# Generated by Django 2.2.4 on 2019-09-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0018_auto_20190804_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zutat',
            name='name',
            field=models.CharField(max_length=60),
        ),
    ]