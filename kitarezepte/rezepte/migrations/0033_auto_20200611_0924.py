# Generated by Django 3.0.6 on 2020-06-11 07:24

from django.db import migrations


def delete_preis(apps, schema_editor):
    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Rezept = apps.get_model('rezepte', 'Rezept')
    Rezept.objects.all().update(_preis=None)


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0032_auto_20200611_0924'),
    ]

    operations = [
        migrations.RunPython(delete_preis),
    ]
