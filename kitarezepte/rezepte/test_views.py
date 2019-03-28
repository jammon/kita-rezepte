# -*- coding: utf-8 -*-
from django.test import TestCase
from rezepte.views import get_client_query_args, menu_array
from rezepte.models import Menue, Rezept


class QueryArgsTestCase(TestCase):
 
    def test_get_client_query_args(self):
        """ Strings are translated to Dates """
        self.assertEqual(get_client_query_args(client_id=5),
                         {'client__id': 5})
        self.assertEqual(get_client_query_args(client_slug='test'),
                         {'client__slug': 'test'})
        self.assertEqual(
            get_client_query_args(client_id=5, client_slug='test'),
            {'client__id': 5, 'client__slug': 'test'})


REZEPT = dict(
            client_id = 1,
            fuer_kinder = 20,
            fuer_erwachsene = 5,
            zubereitung = '',
            anmerkungen = '',
            ist_vorspeise = True,
            ist_hauptgang = False,
            ist_nachtisch = False,
            kategorie = '')

class MenueArrayTestCase(TestCase):
 
    def test_menu_array(self):
        r1 = Rezept.objects.create(titel="Rezept 1", **REZEPT)
        r2 = Rezept.objects.create(titel="Rezept 2", **REZEPT)
        menue = Menue(vorspeise=r1, hauptgang=r2)
        self.assertEqual(
            menu_array(5, menue),
            [5, [r1.id, "Rezept 1"], [r2.id, "Rezept 2"], [0, '']])
        self.assertEqual(
            menu_array(5, None),
            [5, [0, ''], [0, ''], [0, '']])
