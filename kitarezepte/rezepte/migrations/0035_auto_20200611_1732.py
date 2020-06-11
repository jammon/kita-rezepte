# Generated by Django 3.0.6 on 2020-06-11 15:32

from django.db import migrations


def delete_default_preis(apps, schema_editor):
    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Zutat = apps.get_model('rezepte', 'Zutat')
    Zutat.objects.filter(preis_pro_einheit=-1).update(preis=None)


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0034_auto_20200611_1731'),
    ]

    operations = [
        migrations.RunPython(delete_default_preis),
    ]
