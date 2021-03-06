# Generated by Django 2.1.7 on 2019-04-14 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0012_auto_20190329_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editor',
            name='clients',
        ),
        migrations.AddField(
            model_name='editor',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rezepte.Client'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, help_text='wird i.d.R. aus titel berechnet', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='rezept',
            name='anmerkungen',
            field=models.TextField(blank=True, null=True),
        ),
    ]
