# Generated by Django 2.1.7 on 2019-03-26 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0008_auto_20190325_0544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zutatkategorie',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='zutatkategorie',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='zutat',
            name='kategorie',
        ),
        migrations.AddField(
            model_name='zutat',
            name='kategorie',
            field=models.CharField(choices=[('Milch', 'Milchprodukt'), ('Gemüse', 'Gemüse'), ('Obst', 'Obst'), ('Getr.', 'Getreide'), ('Grund.', 'Grundnahrungsmittel'), ('Fisch', 'Fisch'), ('Gewürz', 'Gewürz'), ('Sonst.', 'Sonstiges')], default='', max_length=15),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ZutatKategorie',
        ),
    ]
