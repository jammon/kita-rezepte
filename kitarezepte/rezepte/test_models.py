# -*- coding: utf-8 -*-
from django.test import TestCase
from .models import Client, Zutat, Rezept, RezeptZutat
from .utils import TEST_REIS, TEST_REZEPT


class Zutat_TestCase(TestCase):

    def test_preisInEuro(self):
        """ The price in Euro is displayed correctly """
        zutat = Zutat()
        self.assertEqual(zutat.preisInEuro(), "0,00")
        zutat.preis_pro_einheit = 189
        self.assertEqual(zutat.preisInEuro(), "1,89")

    def test_get_einheit(self):
        """ The unit is displayed correctly """
        zutat = Zutat(einheit="1 Becher")
        self.assertEqual(zutat.get_einheit(), "1 Becher")
        zutat.menge_pro_einheit = 250
        zutat.masseinheit = "g"
        self.assertEqual(zutat.get_einheit(), "g")

    def test_updateRezeptpreise(self):
        """ The price of the recipes is updated """
        reis = Zutat.objects.create(**TEST_REIS)
        rezept = Rezept.objects.create(titel="Reis", **TEST_REZEPT)
        rz = RezeptZutat.objects.create(
            rezept=rezept,
            zutat=reis,
            menge=2000.0,
            nummer=1)
        self.assertEqual(rz.preis(), 378)
        self.assertEqual(rezept.preis(), 378)
        reis.preis_pro_einheit = 179
        reis.save()
        reis.updateRezeptpreise()
        rezept = Rezept.objects.get(pk=rezept.pk)
        self.assertEqual(rezept.preis(), 358)


class Rezept_TestCase(TestCase):

    def test_calculate_slug(self):
        """ The slug is derived from the title """
        ms0 = Rezept.objects.create(titel="Möhren-Salat süß", **TEST_REZEPT)
        ms1 = Rezept.objects.create(titel="Möhren-Salat", **TEST_REZEPT)
        ms2 = Rezept.objects.create(titel="Möhren-Salat", **TEST_REZEPT)
        self.assertEqual(ms0.slug, "möhren-salat-süß")
        self.assertEqual(ms1.slug, "möhren-salat")
        self.assertEqual(ms2.slug, "möhren-salat1")


class RezeptZutat_TestCase(TestCase):

    def test_preis(self):
        reis = Zutat.objects.create(**TEST_REIS)
        rz = RezeptZutat(zutat=reis, menge=500)
        self.assertEqual(rz.preis(), 94)
        self.assertEqual(rz.preisToStr(), "0,94 €")

    def test_str(self):
        reis = Zutat.objects.create(**TEST_REIS)
        rz = RezeptZutat(zutat=reis, menge=500)
        self.assertEqual(str(rz), "500 g Reis")

        rz = RezeptZutat(zutat=reis, menge_qualitativ="etwas")
        self.assertEqual(str(rz), "etwas Reis")
        
        eier = Zutat(name="Eier", client_id=1, einheit="")
        rz = RezeptZutat(zutat=eier, menge=3)
        self.assertEqual(str(rz), "3 Eier")

