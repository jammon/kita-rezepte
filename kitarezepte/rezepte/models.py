# -*- coding: utf-8 -*-
import json
from collections import Counter, defaultdict
from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from .utils import prettyFloat, cent2euro

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


class Client(models.Model):
    """ Ein Mandant, der evtl. mehrere Kitas haben kann """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, blank=True, unique=True,
                            help_text='wird i.d.R. aus dem Namen berechnet')
    mult_providers = models.BooleanField(
        "Mehrere Einrichtungen", default=False)

    class Meta:
        verbose_name = "Mandant"
        verbose_name_plural = "Mandanten"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Provider(models.Model):
    """ Eine Kita, für die geplant wird """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, blank=True, unique=True,
                            help_text='wird i.d.R. aus dem Namen berechnet')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="providers")
    gaenge = models.CharField(
        max_length=50, help_text='z.B. "Vorspeise Hauptgang Nachtisch"',
        default="Vorspeise Hauptgang Nachtisch")
    kategorien = models.CharField(
        max_length=100,
        help_text='z.B. "Reis Teigwaren Getreide Kartoffeln Gemüse '
                  'Suppe Fischgericht Lieblingsgericht"',
        default="", blank=True)
    hidden = models.BooleanField(
        "verborgen",
        default=False,
        help_text='Auf der Hauptseite verbergen')
    _domain = models.CharField("Domain", max_length=32, default="")

    class Meta:
        verbose_name = "Einrichtung"
        verbose_name_plural = "Einrichtungen"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
        self.client.mult_providers = self.client.providers.count() > 1
        self.client.save()

    def get_gaenge(self):
        return self.gaenge.split()

    def get_kategorien(self):
        return self.kategorien.split()

    def main_domain(self):
        return self._domain or self.slug + ".kita-rezepte.de"

    def full_path(self):
        LOCALHOSTS = ("localhost", "127.0.0.1", "kita-rezepte.test")
        domain = self.main_domain()
        for host in LOCALHOSTS:
            if host in domain:
                protocol = 'http://'
                break
        else:
            protocol = 'https://'
        return protocol + domain


class Domain(models.Model):
    """ A Provider can be reached in several domains

    This is for resolution of domain names.
    The main domain of a Provider is provider.main_domain()
    """
    domain = models.CharField(max_length=32)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.domain


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
    preis = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='der Preis einer Packungseinheit; in Euro')
    menge_pro_einheit = models.IntegerField(
        default=0,
        help_text='Anzahl der Maßeinheiten pro Packungseinheit; '
        'bei 1 kg: 1000')
    masseinheit = models.CharField(max_length=5, choices=MASSEINHEITEN)
    kategorie = models.CharField(max_length=30, choices=ZUTATENKATEGORIEN)

    class Meta:
        verbose_name = "Zutat"
        verbose_name_plural = "Zutaten"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.updateRezeptpreise()

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
        for r in self.rezepte.all():
            r.rezept.preis(update=True)

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'einheit': self.einheit,
            'preis': str(self.preis),
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
    # TODO: Löschen nach der Migration
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="rezepte",
        null=True)
    # TODO: remove `null=True` after the migration
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="rezepte",
        null=True)
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
    _preis = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
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
        """ Kategorien als Liste """
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
        """ Gibt den vorberechneten Preis in Euro oder rechnet ihn neu
        """
        if self._preis is None or update:
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
    - menge, menge_qualitativ: die gewünschte Menge als Integer oder
                               qualitativ als String
    - nummer: eine Nummer, um die Zutaten sortieren zu können
    """
    rezept = models.ForeignKey(
        Rezept, on_delete=models.CASCADE, related_name='zutaten')
    zutat = models.ForeignKey(
        Zutat, on_delete=models.CASCADE, related_name='rezepte')
    menge = models.IntegerField(blank=True, null=True)
    menge_qualitativ = models.CharField(max_length=30, blank=True, null=True)
    nummer = models.IntegerField()

    class Meta:
        verbose_name = "Rezeptzutat"
        verbose_name_plural = "Rezeptzutaten"
        ordering = ("nummer",)

    def __str__(self):
        if self.menge_qualitativ is not None:
            return f"{self.menge_qualitativ} {self.zutat.name}"
        if self.menge == 0:
            return f"{self.zutat.name}"
        einheit = self.zutat.get_einheit()
        if einheit:
            return f"{self.menge} {einheit} {self.zutat.name}"
        return f"{self.menge} {self.zutat.name}"

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
        '''Gibt den Preis der Zutat als Decimal in Euro'''
        z = self.zutat
        if self.menge_qualitativ or not self.menge \
                or z.preis is None:
            return Decimal('0.00')
        res = self.menge * z.preis / (z.menge_pro_einheit or 1)
        return res.quantize(Decimal('0.00'))


class GangPlan(models.Model):
    """ Speichert ein Rezept mit Gang (Vorspeise, Hauptgang und Nachtisch)
    und Datum
    """
    # TODO: Löschen nach der Migration
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="menues")
    # TODO: remove `null=True` after the migration
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="menues", null=True)
    datum = models.DateField()
    rezept = models.ForeignKey(Rezept, on_delete=models.CASCADE)
    gang = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Gangplan"
        verbose_name_plural = "Gangpläne"

    def __str__(self):
        return f"Am {self.datum} als {self.gang} {self.rezept.titel}"


def beautify_amounts(messbar):
    units = {'g': 'kg', 'ml': 'l'}
    res = []
    for zutat, menge in messbar.items():
        if zutat.masseinheit in units and menge >= 1000:
            _menge = prettyFloat(menge/1000)
            einheit = units[zutat.masseinheit]
        else:
            _menge = prettyFloat(menge)
            einheit = zutat.masseinheit
        res.append((
            zutat.get_kategorie_display(),
            zutat.name,
            zutat.id,
            _menge,
            einheit))
    return sorted(res)


def get_einkaufsliste(client, start, dauer):
    """ liefert die Daten für /einkaufsliste
    """
    # Für "Folgende Rezepte wurden geplant"
    rezept_plaene = GangPlan.objects.filter(
        provider__client=client,
        datum__gte=start,
        datum__lt=start+timedelta(dauer)
    ).values_list('rezept__titel', 'rezept_id')
    messbar = defaultdict(int)  # Die Zutaten mit quantitativer Mengenangabe
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
        'messbar': beautify_amounts(messbar),
        'qualitativ': sorted(qualitativ.items(), key=key),
        'providers': [p.name for p in client.providers.all()]
                     if client.mult_providers else [],
    }
