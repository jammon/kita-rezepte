# -*- coding: utf-8 -*-
from django import forms

from .models import Zutat, Rezept, MASSEINHEITEN, ZUTATENKATEGORIEN

class ZutatForm(forms.ModelForm):
    class Meta:
        model = Zutat
        fields = ('name', 'einheit', 'preis_pro_einheit', 'menge_pro_einheit', 
                  'masseinheit', 'kategorie')
        labels = {
            'name': 'Zutat',
            'einheit': 'Packungseinheit',
            'preis_pro_einheit': 'Preis pro Einheit',
            'menge_pro_einheit': 'Menge pro Einheit',
            'masseinheit': 'Maßeinheit',
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

