# -*- coding: utf-8 -*-
from datetime import date
from django.test import TestCase
from .models import Client, Zutat, Rezept, RezeptZutat, GangPlan, get_einkaufsliste
from .utils import TEST_REIS, TEST_REZEPT


class Zutat_TestCase(TestCase):

    def test_preisInEuro(self):
        """ The price in Euro is displayed correctly """
        zutat = Zutat()
        self.assertEqual(zutat.preisInEuro(), "--")
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
        self.assertEqual(ms0.slug, "moehren-salat-suess")
        self.assertEqual(ms1.slug, "moehren-salat")
        self.assertEqual(ms2.slug, "moehren-salat1")


class RezeptZutat_TestCase(TestCase):

    def test_preis(self):
        reis = Zutat.objects.create(**TEST_REIS)
        rz = RezeptZutat(zutat=reis, menge=500)
        self.assertEqual(rz.preis(), 94)
        self.assertEqual(rz.preisToStr(), "0,94 €")

        rz = RezeptZutat(zutat=reis, menge_qualitativ="etwas")
        self.assertEqual(rz.preis(), 0)
        self.assertEqual(rz.preisToStr(), "0,00 €")

    def test_str(self):
        reis = Zutat.objects.create(**TEST_REIS)
        rz = RezeptZutat(zutat=reis, menge=500)
        self.assertEqual(str(rz), "500 g Reis")

        rz = RezeptZutat(zutat=reis, menge_qualitativ="etwas")
        self.assertEqual(str(rz), "etwas Reis")
        
        eier = Zutat(name="Eier", client_id=1, einheit="")
        rz = RezeptZutat(zutat=eier, menge=3)
        self.assertEqual(str(rz), "3 Eier")


class Get_Einkaufsliste_TestCase(TestCase):

    def test_get_einkaufsliste(self):
        client = Client.objects.create(
            name="Test", slug="test", gaenge="Vorspeise Hauptgang Nachtisch")
        
        reis = Zutat.objects.create(name="Reis", 
            client = client,
            einheit="1 kg",
            preis_pro_einheit=189,
            menge_pro_einheit=1000,
            masseinheit="g",
            kategorie="Grund.")
        wasser = Zutat.objects.create(name="Wasser", 
            client = client,
            einheit="1 l",
            preis_pro_einheit=10,
            menge_pro_einheit=1000,
            masseinheit="ml",
            kategorie="Grund.")
        milch = Zutat.objects.create(name="Milch", 
            client = client,
            einheit="1 l",
            preis_pro_einheit=129,
            menge_pro_einheit=1000,
            masseinheit="ml",
            kategorie="Milchprodukte")
        
        args = dict(client = client, fuer_kinder=20, fuer_erwachsene=5, zubereitung='')
        wasserreis = Rezept.objects.create(titel="Wasserreis", **args)
        milchreis = Rezept.objects.create(titel="Milchreis", **args)
        
        RezeptZutat.objects.bulk_create([
            RezeptZutat(rezept=wasserreis, zutat=reis, menge=500.0, nummer=1),
            RezeptZutat(rezept=wasserreis, zutat=wasser, menge=2000.0, nummer=2),
            RezeptZutat(rezept=milchreis, zutat=reis, menge=400.0, nummer=1),
            RezeptZutat(rezept=milchreis, zutat=milch, menge=2000.0, nummer=2),
            RezeptZutat(rezept=milchreis, zutat=wasser, menge_qualitativ="etwas", nummer=3),
        ])
        args = dict(client = client, gang="Hauptgang")
        GangPlan.objects.bulk_create([
            GangPlan(datum=date(2019, 5, 31), rezept=milchreis, **args),
            GangPlan(datum=date(2019, 6, 1), rezept=wasserreis, **args),
            GangPlan(datum=date(2019, 6, 2), rezept=milchreis, **args),
            GangPlan(datum=date(2019, 6, 3), rezept=wasserreis, **args),
        ])
        el = get_einkaufsliste('test', date(2019, 5, 31), 3)

        self.assertEqual(
            el['rezepte'],
            [("Milchreis", milchreis.id), ("Wasserreis", wasserreis.id)])
        self.assertEqual(
            el['messbar'],
            [(reis, '1300'), (wasser, '2000'), (milch, '4000')])
        self.assertEqual(
            el['qualitativ'],
            [(wasser, ['etwas', 'etwas'])])


