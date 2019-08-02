# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE

from .models import Zutat, Rezept, MASSEINHEITEN, ZUTATENKATEGORIEN


class ZutatForm(forms.ModelForm):
    masseinheit = forms.ChoiceField(
        choices=MASSEINHEITEN,
        widget=forms.RadioSelect)
    kategorie = forms.ChoiceField(
        choices=ZUTATENKATEGORIEN,
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
    gang_list = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Gang',
    )

    class Meta:
        model = Rezept
        fields = ('titel', 'untertitel', 'fuer_kinder', 'fuer_erwachsene',
                  'zubereitung', 'anmerkungen', 'kategorie', 'gang_list')
        labels = {
            'fuer_kinder': 'Anzahl Kinder', 
            'fuer_erwachsene': 'Anzahl Erwachsene', 
            'kategorie': 'Kategorie',
        }
        widgets = {
            'zubereitung': TinyMCE(attrs={'cols': 50, 'rows': 12}),
            'anmerkungen': TinyMCE(attrs={'cols': 50, 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        default_gaenge = [(g, g) for g in ['Vorspeise', 'Hauptgang', 'Nachtisch']]
        gaenge = kwargs.pop('gaenge', default_gaenge)
        super().__init__(*args, **kwargs)
        self.fields['gang_list'].choices = gaenge

    def get_initial_for_field(self, field, field_name):
        if field_name=='gang_list':
            return self.instance.gang_list
        return super().get_initial_for_field(field, field_name)

    def clean(self):
        cleaned_data = super().clean()
        self.instance.gang_list = cleaned_data['gang_list']
        return cleaned_data