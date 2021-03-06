# Generated by Django 3.0.6 on 2020-07-27 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rezepte', '0030_auto_20200626_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, help_text='wird i.d.R. aus dem Namen berechnet', max_length=30, unique=True),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, help_text='wird i.d.R. aus dem Namen berechnet', max_length=30, unique=True)),
                ('gaenge', models.CharField(default='Vorspeise Hauptgang Nachtisch', help_text='z.B. "Vorspeise Hauptgang Nachtisch"', max_length=50)),
                ('kategorien', models.CharField(blank=True, default='', help_text='z.B. "Reis Teigwaren Getreide Kartoffeln Gemüse Suppe Fischgericht Lieblingsgericht"', max_length=100)),
                ('hidden', models.BooleanField(default=False, help_text='Auf der Hauptseite verbergen', verbose_name='verborgen')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rezepte.Client')),
            ],
            options={
                'verbose_name': 'Einrichtung',
                'verbose_name_plural': 'Einrichtungen',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=32)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rezepte.Provider')),
            ],
        ),
        migrations.AddField(
            model_name='gangplan',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menues', to='rezepte.Provider'),
        ),
        migrations.AddField(
            model_name='rezept',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rezepte', to='rezepte.Provider'),
        ),
    ]
