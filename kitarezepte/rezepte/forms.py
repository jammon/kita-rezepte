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
        fields = ('name', 'einheit', 'preis', 'menge_pro_einheit',
                  'masseinheit', 'kategorie')
        labels = {
            'name': 'Zutat',
            'einheit': 'Packungseinheit',
            'preis': 'Preis pro Einheit',
            'menge_pro_einheit': 'Menge pro Einheit',
            'kategorie': 'Kategorie',
        }


class RezeptForm(forms.ModelForm):
    gang_list = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Gang',
    )
    kategorie_list = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Kategorie',
        required=False,
    )

    class Meta:
        model = Rezept
        fields = ('titel', 'untertitel', 'fuer_kinder', 'fuer_erwachsene',
                  'zubereitung', 'anmerkungen', 'kategorie_list', 'gang_list')
        labels = {
            'fuer_kinder': 'Anzahl Kinder',
            'fuer_erwachsene': 'Anzahl Erwachsene',
        }
        widgets = {
            'zubereitung': TinyMCE(attrs={'cols': 50, 'rows': 12}),
            'anmerkungen': TinyMCE(attrs={'cols': 50, 'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session')
        super().__init__(*args, **kwargs)
        self.fields['gang_list'].choices = [
            (g, g) for g in session.get('gaenge', [])]
        self.fields['kategorie_list'].choices = [
            (k, k) for k in session.get('kategorien', [])]

    def get_initial_for_field(self, field, field_name):
        if field_name == 'gang_list':
            return self.instance.gang_list
        if field_name == 'kategorie_list':
            return self.instance.kategorie_list
        return super().get_initial_for_field(field, field_name)

    def clean(self):
        cleaned_data = super().clean()
        self.instance.gang_list = cleaned_data.get('gang_list', [])
        self.instance.kategorie_list = cleaned_data.get('kategorie_list', [])
        return cleaned_data
