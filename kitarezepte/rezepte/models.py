# -*- coding: utf-8 -*-
import json
import re
from collections import Counter, defaultdict
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .utils import prettyFloat, cent2euro, get_client_domain

REZEPTKATEGORIEN = (
    ("Reis", "Reis"),
    ("Teigw.", "Teigwaren"),
    ("Getr.", "Getreide"),
    ("Kart.", "Kartoffeln"),
    ("Gemüse", "Gemüse"),
    ("Suppe", "Suppe"),
    ("Fisch", "Fischgericht"),
    ("Liebl.", "Lieblingsgericht"),
)

GAENGE = ('Vorspeise', 'Hauptgang', 'Nachtisch')

MASSEINHEITEN = [(s, s) for s in ("g", "ml", "St.", "Pckg.")]

ZUTATENKATEGORIEN = (
    ("Milch", "Milchprodukt"),
    ("Gemüse", "Gemüse"),
    ("Obst", "Obst"),
    ("Getr.", "Getreide"),
    ("Grund.", "Grundnahrungsmittel"),
    ("Fisch", "Fisch"),
    ("Gewürz", "Gewürz"),
    ("Sonst.", "Sonstiges"),
)

KEIN_PREIS = -1


class Client(models.Model):
    """ Eine Kita, für die geplant wird """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, blank=True, unique=True,
                            help_text='wird i.d.R. aus titel berechnet')
    gaenge = models.CharField(
        max_length=50, help_text='z.B. "Vorspeise Hauptgang Nachtisch"',
        default="Vorspeise Hauptgang Nachtisch")
    kategorien = models.CharField(
        max_length=100,
        help_text='z.B. "Reis Teigwaren Getreide Kartoffeln Gemüse '
                  'Suppe Fischgericht Lieblingsgericht"',
        default="", blank=True)

    class Meta:
        verbose_name = "Mandant"
        verbose_name_plural = "Mandanten"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_domain(self):
        return get_client_domain(self.slug)

    def get_gaenge(self):
        return self.gaenge.split()

    def get_kategorien(self):
        return self.kategorien.split()


class Editor(models.Model):
    user = models.OneToOneField(
        User, related_name='editor', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        name = self.user.get_full_name() or self.user.get_username()
        return f"{name} ist Editor für {self.client.name}"


class Zutat(models.Model):
    """ Eine Zutat, die in den Rezepten verwandt werden kann """
    name = models.CharField(max_length=60)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="zutaten")
    einheit = models.CharField(
        max_length=30, default='', blank=True,
        help_text='''Packungseinheit für den Einkauf meist 1 kg, 1 l,
             aber auch 2,5 kg-Sack.
             Fällt weg bei Dingen wie Eiern, die eine natürliche Einheit
             haben; dann "Stück"''')
    preis_pro_einheit = models.IntegerField(
        default=KEIN_PREIS,
        help_text='der Preis einer Packungseinheit; in Cent')
    menge_pro_einheit = models.IntegerField(
        default=0,
        help_text='Anzahl der Maßeinheiten pro Packungseinheit; '
        'bei 1 kg: 1000')
    masseinheit = models.CharField(max_length=5, choices=MASSEINHEITEN)
    kategorie = models.CharField(max_length=15, choices=ZUTATENKATEGORIEN)

    class Meta:
        verbose_name = "Zutat"
        verbose_name_plural = "Zutaten"

    def __str__(self):
        return self.name

    def preisInEuro(self):
        """ Preis einer Packungseinheit in Euro als String

        z.B. "3,59"
        """
        if self.preis_pro_einheit == KEIN_PREIS:
            return "--"
        return cent2euro(self.preis_pro_einheit)

    def get_einheit(self):
        if self.menge_pro_einheit:
            return self.masseinheit
        else:
            return self.einheit

    def updateRezeptpreise(self):
        """ Wenn der Preis einer Zutat geändert wurde,
        müssen die Rezeptpreise entsprechend angepasst werden.

        TODO: Dies macht für jedes Rezept
        - eine Abfrage nach den Zutaten und
        - ein save
        """
        for rz in self.rezepte.all():
            rz.rezept.preis(update=True)

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'einheit': self.einheit,
            'preis_pro_einheit': self.preis_pro_einheit,
            'menge_pro_einheit': self.menge_pro_einheit,
            'masseinheit': self.masseinheit,
            'kategorie': self.kategorie,
        })

TRANSTABLE = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
              'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue',
              'ß': 'ss',
              'é': 'e', 'è': 'e', 'à': 'a',
              'É': 'e', 'È': 'e', 'À': 'a',
              }
translate_specials = str.maketrans(TRANSTABLE)


class Rezept(models.Model):
    '''Enthält ein Rezept mit Titel, Kochanweisung usw.
       Die Zutaten werden getrennt davon mit dem Key des Rezepts gespeichert
       (Model RezeptZutat).
    '''
    titel = models.CharField(max_length=100)
    untertitel = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="rezepte")
    slug = models.SlugField(
        max_length=100, blank=True,
        help_text='wird i.d.R. aus titel berechnet')
    fuer_kinder = models.IntegerField(help_text="Anzahl der Kinder")
    fuer_erwachsene = models.IntegerField(help_text="Anzahl der Erwachsenen")
    zubereitung = models.TextField()
    anmerkungen = models.TextField(null=True, blank=True)
    eingegeben_von = models.ForeignKey(User, on_delete=models.SET_NULL,
                                       null=True, blank=True)
    gang = models.CharField(
        max_length=40,
        help_text='Der Gang, für den das Rezept geeignet ist, '
        'ggf. eine Leerzeichen-getrennte Liste mehrerer Gänge')
    kategorien = models.CharField(
        max_length=60,
        help_text='Die Kategorie, zu der das Rezept gehört, '
        'ggf. eine Leerzeichen-getrennte Liste mehrerer Kategorien',
        default='', blank=True)
    # z.B. Gemüse, Teigwaren, Suppe, Getreide, Reis usw.
    _preis = models.IntegerField(
        default=KEIN_PREIS,
        help_text='kann leer sein, wird dann automatisch berechnet')

    class Meta:
        verbose_name = "Rezept"
        verbose_name_plural = "Rezepte"

    @property
    def gang_list(self):
        """ Gänge als Liste """
        return self.gang.split()

    @gang_list.setter
    def gang_list(self, values):
        self.gang = ' '.join(values)

    @property
    def kategorie_list(self):
        """ Gänge als Liste """
        return self.kategorien.split()

    @kategorie_list.setter
    def kategorie_list(self, values):
        self.kategorien = ' '.join(values)

    def __str__(self):
        return self.titel

    def save(self, *args, **kwargs):
        if not self.pk:
            self.calculate_slug()
        super().save(*args, **kwargs)

    def calculate_slug(self):
        """Errechnet ein slug, das aus dem Titel erstellt wird und noch nicht
        vergeben ist.
        """
        # Slug erstellen und Sonderzeichen ersetzen
        self.slug = slug = (
            slugify(self.titel, allow_unicode=True) or 'kein-titel'
            ).translate(translate_specials)
        # Alle Slugs raussuchen, die genau so anfangen
        existing_slugs = Rezept.objects.all().filter(slug__startswith=slug)\
            .exclude(pk=self.pk)\
            .order_by('slug')\
            .values_list('slug', flat=True)
        if len(existing_slugs) > 0 and slug in existing_slugs:
            i = 1
            while slug + str(i) in existing_slugs:
                i += 1
            self.slug = slug + str(i)

    def preis(self, update=False):
        """ Gibt den vorberechneten Preis in Cent oder rechnet ihn neu
        """
        if self._preis == KEIN_PREIS or update:
            self._preis = sum(
                [zutat.preis() for zutat in self.zutaten.all()])
            if self.pk:
                self.save()
        return self._preis

    def preisToStr(self):
        """ Gibt den Preis als String (z.B. '13,48 €')
        """
        return cent2euro(self.preis()) + " €"


class RezeptZutat(models.Model):
    """Eine Zutat, die in einem Rezept verwendet wird.

    Enthält
    - rezept, zutat: einen Verweis auf das Rezept und die Zutat
    - menge, menge_qualitativ: die gewünschte Menge als Float oder
                               qualitativ als String
    - nummer: eine Nummer, um die Zutaten sortieren zu können
    """
    rezept = models.ForeignKey(
        Rezept, on_delete=models.CASCADE, related_name='zutaten')
    zutat = models.ForeignKey(
        Zutat, on_delete=models.CASCADE, related_name='rezepte')
    menge = models.FloatField(blank=True, null=True)
    menge_qualitativ = models.CharField(max_length=30, blank=True, null=True)
    nummer = models.IntegerField()

    class Meta:
        verbose_name = "Rezeptzutat"
        verbose_name_plural = "Rezeptzutaten"
        ordering = ("nummer",)

    def __str__(self):
        if self.menge_qualitativ:
            return f"{self.menge_qualitativ} {self.zutat.name}"
        if self.menge == 0:
            return f"{self.zutat.name}"
        menge = prettyFloat(self.menge)
        einheit = self.zutat.get_einheit()
        if einheit:
            return f"{menge} {einheit} {self.zutat.name}"
        return f"{menge} {self.zutat.name}"

    def toJson(self):
        res = {
            'rezept_id': self.rezept_id,
            'zutat_id': self.zutat_id,
            'nummer': self.nummer,
        }
        if self.menge:
            res['menge'] = self.menge
        else:
            res['menge_qualitativ'] = self.menge_qualitativ or ''
        return json.dumps(res)

    def preis(self):
        '''Gibt den Preis der Zutat in Cent'''
        if self.menge_qualitativ or not self.menge:
            return 0
        z = self.zutat
        if z.preis_pro_einheit == KEIN_PREIS:
            return 0
        return int(self.menge * z.preis_pro_einheit //
                   (z.menge_pro_einheit or 1))

    def preisToStr(self):
        return cent2euro(self.preis()) + " €"


class GangPlan(models.Model):
    """ Speichert ein Rezept mit Gang (Vorspeise, Hauptgang und Nachtisch)
    und Datum
    """
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="menues")
    datum = models.DateField()
    rezept = models.ForeignKey(Rezept, on_delete=models.CASCADE)
    gang = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Gangplan"
        verbose_name_plural = "Gangpläne"

    def __str__(self):
        return f"Am {self.datum} als {self.gang} {self.rezept.titel}"


def get_einkaufsliste(client_slug, start, dauer):
    """ liefert die Daten für /einkaufsliste
    """
    # Für "Folgende Rezepte wurden geplant"
    rezept_plaene = GangPlan.objects.filter(
        client__slug=client_slug,
        datum__gte=start,
        datum__lt=start+timedelta(dauer)
    ).values_list('rezept__titel', 'rezept_id')
    messbar = defaultdict(float)  # Die Zutaten mit quantitativer Mengenangabe
    qualitativ = defaultdict(list)  # Die Zutaten mit qualitativer Mengenangabe
    rezeptcounts = Counter([p[1] for p in rezept_plaene])
    rezeptzutaten = RezeptZutat.objects.filter(
        rezept_id__in=rezeptcounts.keys()
    ).select_related('zutat')

    for rz in rezeptzutaten:
        # Wenn messbar:
        if rz.menge:
            # Zutat mit Mengenangabe aufsummieren
            messbar[rz.zutat] += rz.menge * rezeptcounts[rz.rezept_id]
        # sonst:
        else:
            # Zutat mit qualitativer Mengenangabe abspeichern
            qualitativ[rz.zutat].extend(
                [rz.menge_qualitativ] * rezeptcounts[rz.rezept_id])

    def key(item):
        zutat = item[0]
        return zutat.kategorie, zutat.name

    return {
        'start': start,
        'dauer': dauer,
        'rezepte': sorted(set(rezept_plaene)),
        'messbar': sorted(((zutat, prettyFloat(menge))
                           for zutat, menge in messbar.items()),
                          key=key),
        'qualitativ': sorted(qualitativ.items(), key=key)
    }
