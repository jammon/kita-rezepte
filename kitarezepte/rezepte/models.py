# -*- coding: utf-8 -*-
import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

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

class Gang(models.Model):
    """ Ein Gang, der geplant werden kann. 

    Z.B. Frühstück, Vorspeise etc. Wird nötig für weitere Kunden.
    """
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Gang"
        verbose_name_plural = "Gänge"

    def __str__(self):
        return self.name
    
class Client(models.Model):
    """ Eine Kita, für die geplant wird """
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=30, blank=True,
                            help_text='wird i.d.R. aus titel berechnet')
    gaenge = models.ManyToManyField(Gang)

    class Meta:
        verbose_name = "Mandant"
        verbose_name_plural = "Mandanten"

    def __str__(self):
        return self.name
    

class Editor(models.Model):
    user = models.OneToOneField(
        User, related_name='editor', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)


class Zutat(models.Model):
    """ Eine Zutat, die in den Rezepten verwandt werden kann """
    name = models.CharField(max_length=25)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="zutaten")
    einheit = models.CharField(
        max_length=10, default='',
        help_text='''Packungseinheit für den Einkauf meist 1 kg, 1 l,
             aber auch 2,5 kg-Sack.
             Fällt weg bei Dingen wie Eiern, die eine natürliche Einheit
             haben; dann "Stück"''')
    preis_pro_einheit = models.IntegerField(
        default=0,
        help_text='der Preis einer Packungseinheit; in Cent')
    menge_pro_einheit = models.IntegerField(
        default=0,
        help_text='Anzahl der Masseinheiten (s.u.) pro Packungseinheit; '
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
        return cent2euro(self.preis_pro_einheit)

    def get_einheit(self):
        if self.menge_pro_einheit:
            return self.masseinheit
        else:
            return self.einheit

    def updateRezeptpreise(self):
        """ Wenn der Preis einer Zutat geändert wurde,
        müssen die Rezeptpreise entsprechend angepasst werden.
        """
        for rz in self.rezepte.all():
            rz.rezept.preis(update=True)


class RezeptKategorie(TaggedItemBase):
    content_object = models.ForeignKey('Rezept', on_delete=models.CASCADE)


class Rezept(models.Model):
    '''Enthält ein Rezept mit Titel, Kochanweisung usw.
       Die Zutaten werden getrennt davon mit dem Key des Rezepts gespeichert
       (Model RezeptZutat).
    '''
    titel = models.CharField(max_length=30)
    untertitel = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="rezepte")
    slug = models.SlugField(
        max_length=30, blank=True, help_text='wird i.d.R. aus titel berechnet')
    fuer_kinder = models.IntegerField(help_text="Anzahl der Kinder")
    fuer_erwachsene = models.IntegerField(help_text="Anzahl der Erwachsenen")
    # zutaten = models.ManyToManyField(
    #     Zutat, through='RezeptZutat', related_name='rezepte')
    zubereitung = models.TextField()
    anmerkungen = models.TextField()
    eingegeben_von = models.ForeignKey(User, on_delete=models.SET_NULL,
                                       null=True, blank=True)
    ist_vorspeise = models.BooleanField(help_text="kann als Vorspeise dienen")
    ist_hauptgang = models.BooleanField(help_text="kann als Hauptgang dienen")
    ist_nachtisch = models.BooleanField(help_text="kann als Nachtisch dienen")
    kategorie = TaggableManager(verbose_name='Kategorie',
                                help_text="Art des Essens",
                                through=RezeptKategorie)
    # z.B. Gemüse, Teigwaren, Suppe, Getreide, Reis usw.
    _preis = models.IntegerField(
        default=0,
        help_text='kann leer sein, wird dann automatisch berechnet')

    class Meta:
        verbose_name = "Rezept"
        verbose_name_plural = "Rezepte"

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
        self.slug = slug = slugify(self.titel, allow_unicode=True)
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
        if self._preis == 0 or update:
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
    menge_qualitativ = models.CharField(max_length=15, blank=True, null=True)
    nummer = models.IntegerField()

    class Meta:
        verbose_name = "Rezeptzutat"
        verbose_name_plural = "Rezeptzutaten"
        ordering = ("nummer",)

    def __str__(self):
        if self.menge_qualitativ:
            elements = [self.menge_qualitativ]
        else:
            elements = [prettyFloat(self.menge)]
            einheit = self.zutat.get_einheit()
            if einheit:
                elements.append(einheit)
        elements.append(self.zutat.name)
        return " ".join(elements)

    def preis(self):
        '''Gibt den Preis der Zutat in Cent'''
        if self.menge_qualitativ:
            return 0
        z = self.zutat
        return int(self.menge * z.preis_pro_einheit //
                   (z.menge_pro_einheit or 1))

    def preisToStr(self):
        return cent2euro(self.preis()) + " €"


class Menue(models.Model):
    """ Speichert drei Rezepte (Vorspeise, Hauptgang und Nachtisch),
    einen Koch und eine Bewertung

    Zusätzlich werden Listen der Gänge, Titel der Gänge und
    Preise der Gänge gespeichert.
    Die Änderungsoperationen sollen immer auf den einzelnen
    Rezept-Properties erfolgen.
    """
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="menues")
    datum = models.DateField(null=True)
    koch = models.CharField(max_length=20, null=True, blank=True)
    vorspeise = models.ForeignKey(
        Rezept, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="vorspeise")
    hauptgang = models.ForeignKey(
        Rezept, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="hauptgang")
    nachtisch = models.ForeignKey(
        Rezept, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="nachtisch")
    geschlossen = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Menü"
        verbose_name_plural = "Menüs"

    def get_gang(self, nr):
        return getattr(self, ('vorspeise', 'hauptgang', 'nachtisch')[nr])

    def get_gang_titel(self, nr):
        gang = self.get_gang(nr)
        return gang.titel if gang else ''

    def get_gang_titel(self, nr, mit_preis=False):
        gang = self.get_gang(nr)
        if gang:
            if mit_preis:
                return gang.titel + " " + gang.preisToStr()
            return gang.titel
        return ''

