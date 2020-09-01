# -*- coding: utf-8 -*-
from datetime import date
from decimal import Decimal
from django.test import TestCase
from .models import (
    Client, Provider, Zutat, Rezept, RezeptZutat, GangPlan,
    get_einkaufsliste)
from .utils import TEST_REIS, TEST_REZEPT


class Zutat_TestCase(TestCase):

    def test_get_einheit(self):
        """ The unit is displayed correctly """
        zutat = Zutat(einheit="1 Becher")
        self.assertEqual(zutat.get_einheit(), "1 Becher")
        zutat.menge_pro_einheit = 250
        zutat.masseinheit = "g"
        self.assertEqual(zutat.get_einheit(), "g")

    def test_updateRezepte(self):
        """ The price of the recipes is updated """
        client = Client.objects.create(name='Test-Kita')
        provider = Provider.objects.create(name='Test-Kita', client=client)
        reis = Zutat.objects.create(client=client, **TEST_REIS)
        rezept = Rezept.objects.create(
            titel="Reis", client=client, **TEST_REZEPT)
        rz = RezeptZutat.objects.create(
            rezept=rezept,
            zutat=reis,
            menge=2000,
            nummer=1)
        self.assertEqual(rz.preis(), Decimal('3.78'))
        self.assertEqual(rezept.preis(), Decimal('3.78'))
        reis.preis = Decimal('1.79')
        reis.save()
        reis.updateRezepte()
        rezept = Rezept.objects.get(pk=rezept.pk)
        self.assertEqual(rezept.preis(), Decimal('3.58'))


class Rezept_TestCase(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name='Test-Kita')
        self.provider = Provider.objects.create(
            name='Test-Kita', client=self.client)

    def test_calculate_slug(self):
        """ The slug is derived from the title """
        for titel, slug in (
                ("Möhren-Salat süß", "moehren-salat-suess"),
                ("Möhren-Salat", "moehren-salat"),
                ("Möhren-Salat", "moehren-salat1"),
        ):
            rezept = Rezept.objects.create(
                titel=titel, provider=self.provider, **TEST_REZEPT)
            self.assertEqual(rezept.slug, slug)

    def test_updateRezepte(self):
        reis = Zutat.objects.create(client=self.client, **TEST_REIS)
        rezept = Rezept.objects.create(
            titel="Reis", provider=self.provider, **TEST_REZEPT)
        RezeptZutat.objects.create(
            rezept=rezept, zutat=reis, menge=500, nummer=1)
        self.assertEqual(reis.rezepte.count(), 1)
        self.assertEqual(rezept.preis(update=True), Decimal('0.94'))

        reis.preis = Decimal('2.00')
        reis.save()
        rezept = Rezept.objects.get(pk=rezept.pk)
        self.assertEqual(rezept.preis(update=False), Decimal('1.00'))

    def test_allergene(self):
        sosse = Zutat.objects.create(
            name='Soße',
            client=self.client,
            allergene=Zutat.GLUTEN + Zutat.SENF + Zutat.SELLERIE)
        eier = Zutat.objects.create(
            name='Eier',
            client=self.client,
            allergene=Zutat.EIER)
        rezept = Rezept.objects.create(
            titel="Eier mit Soße", provider=self.provider, **TEST_REZEPT)
        RezeptZutat.objects.create(
            rezept=rezept, zutat=eier, menge=2, nummer=1)
        RezeptZutat.objects.create(
            rezept=rezept, zutat=sosse, menge_qualitativ='etwas', nummer=2)
        rezept.save()
        for allergen, present in (
            (Zutat.GLUTEN, True),
            (Zutat.KREBSTIERE, False),
            (Zutat.EIER, True),
            (Zutat.FISCH, False),
            (Zutat.ERDNUESSE, False),
            (Zutat.SOJA, False),
            (Zutat.MILCH, False),
            (Zutat.NUESSE, False),
            (Zutat.SELLERIE, True),
            (Zutat.SENF, True),
            (Zutat.SESAM, False),
            (Zutat.SULPHITE, False),
            (Zutat.LUPINEN, False),
            (Zutat.WEICHTIERE, False),
        ):
            self.assertEqual(allergen in rezept.allergene, present)
        self.assertEqual(
            rezept.get_allergene(),
            "Gluten, Eier, Sellerie, Senf")


class RezeptZutat_TestCase(TestCase):
    def setUp(self):
        self.kitaclient = Client.objects.create(name='Test-Kita')
        self.reis = Zutat(client=self.kitaclient, **TEST_REIS)

    def test_preis(self):
        rz = RezeptZutat(zutat=self.reis, menge=500)
        self.assertEqual(rz.preis(), Decimal('0.94'))

        rz = RezeptZutat(zutat=self.reis, menge_qualitativ="etwas")
        self.assertEqual(rz.preis(), Decimal('0.00'))

    def test_str(self):
        rz = RezeptZutat(zutat=self.reis, menge=500)
        self.assertEqual(str(rz), "500 g Reis")

        rz = RezeptZutat(zutat=self.reis, menge_qualitativ="etwas")
        self.assertEqual(str(rz), "etwas Reis")

        eier = Zutat(name="Eier", client=self.kitaclient, einheit="")
        rz = RezeptZutat(zutat=eier, menge=3)
        self.assertEqual(str(rz), "3 Eier")


class Get_Einkaufsliste_TestCase(TestCase):

    def test_get_einkaufsliste(self):
        client = Client.objects.create(name="Test", slug="test")
        provider = Provider.objects.create(name='Test', client=client)

        reis = Zutat.objects.create(name="Reis",
                                    client=client,
                                    einheit="1 kg",
                                    preis=Decimal('1.89'),
                                    menge_pro_einheit=1000,
                                    masseinheit="g",
                                    kategorie="Grundnahrungsmittel")
        wasser = Zutat.objects.create(name="Wasser",
                                      client=client,
                                      einheit="1 l",
                                      preis=Decimal('0.10'),
                                      menge_pro_einheit=1000,
                                      masseinheit="ml",
                                      kategorie="Grundnahrungsmittel")
        milch = Zutat.objects.create(name="Milch",
                                     client=client,
                                     einheit="1 l",
                                     preis=Decimal('1.29'),
                                     menge_pro_einheit=1000,
                                     masseinheit="ml",
                                     kategorie="Milchprodukte")

        args = dict(client=client, provider=provider, fuer_kinder=20,
                    fuer_erwachsene=5, zubereitung='')
        wasserreis = Rezept.objects.create(titel="Wasserreis", **args)
        milchreis = Rezept.objects.create(titel="Milchreis", **args)

        RezeptZutat.objects.bulk_create([
            RezeptZutat(rezept=wasserreis, zutat=reis, menge=500, nummer=1),
            RezeptZutat(rezept=wasserreis, zutat=wasser, menge=2000, nummer=2),
            RezeptZutat(rezept=milchreis, zutat=reis, menge=400, nummer=1),
            RezeptZutat(rezept=milchreis, zutat=milch, menge=400, nummer=2),
            RezeptZutat(rezept=milchreis, zutat=wasser, menge_qualitativ="etwas", nummer=3),
        ])
        args = dict(client=client, provider=provider, gang="Hauptgang")
        GangPlan.objects.bulk_create([
            GangPlan(datum=date(2019, 5, 31), rezept=milchreis, **args),
            GangPlan(datum=date(2019, 6, 1), rezept=wasserreis, **args),
            GangPlan(datum=date(2019, 6, 2), rezept=milchreis, **args),
            GangPlan(datum=date(2019, 6, 3), rezept=wasserreis, **args),
        ])
        el = get_einkaufsliste(client, date(2019, 5, 31), 3)

        self.assertEqual(
            el['rezepte'],
            [("Milchreis", milchreis.id), ("Wasserreis", wasserreis.id)])
        self.assertEqual(
            el['messbar'],
            [('Grundnahrungsmittel', 'Reis', reis.id, '1,3', 'kg'),
             ('Grundnahrungsmittel', 'Wasser', wasser.id, '2', 'l'),
             ('Milchprodukte', 'Milch', milch.id, '800', 'ml')])
        self.assertEqual(
            el['qualitativ'],
            [(wasser, ['etwas', 'etwas'])])
