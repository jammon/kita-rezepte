# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE

from .models import Zutat, Rezept, MASSEINHEITEN, ZUTATENKATEGORIEN


class ZutatForm(forms.ModelForm):
    masseinheit = forms.ChoiceField(
        choices=MASSEINHEITEN,
        widget=forms.RadioSelect)

    class Meta:
        model = Zutat
        fields = ('name', 'einheit', 'preis_pro_einheit', 'menge_pro_einheit', 
                  'masseinheit', 'kategorie')
        labels = {
            'name': 'Zutat',
            'einheit': 'Packungseinheit',
            'preis_pro_einheit': 'Preis pro Einheit',
            'menge_pro_einheit': 'Menge pro Einheit',
            'kategorie': 'Kategorie',
        }


class RezeptForm(forms.ModelForm):
    class Meta:
        model = Rezept
        fields = ('titel', 'untertitel', 'fuer_kinder', 'fuer_erwachsene',
                  'zubereitung', 'anmerkungen')
        labels = {
            'fuer_kinder': 'Anzahl Kinder', 
            'fuer_erwachsene': 'Anzahl Erwachsene', 
        }
        widgets = {
            'zubereitung': TinyMCE(attrs={'cols': 50, 'rows': 20}),
            'anmerkungen': TinyMCE(attrs={'cols': 50, 'rows': 10}),
        }

