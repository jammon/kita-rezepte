# -*- coding: utf-8 -*-
from datetime import date
from django.test import TestCase
from rezepte.utils import str2date, prettyFloat, days_in_month


class Str2dateTestCase(TestCase):
 
    def test_str2date(self):
        """ Strings are translated to Dates """
        self.assertEqual(str2date("22.3.2019"), date(2019, 3, 22))
        self.assertEqual(str2date("22.03.2019"), date(2019, 3, 22))
        self.assertEqual(str2date("1.1.2019"), date(2019, 1, 1))
        self.assertEqual(str2date("31.12.2019"), date(2019, 12, 31))


class PrettyFloatTestCase(TestCase):
 
    def test_prettyFloat(self):
        """ stringified floats are pretty """
        self.assertEqual(prettyFloat(3.0), "3")
        self.assertEqual(prettyFloat(3.1), "3.1")


class Days_in_MonthTestCase(TestCase):
 
    def test_days_in_month(self):
        """ correct day count """
        self.assertEqual(days_in_month(2019, 1), 31)
        self.assertEqual(days_in_month(2019, 2), 28)
        self.assertEqual(days_in_month(2019, 3), 31)
        self.assertEqual(days_in_month(2019, 11), 30)
        self.assertEqual(days_in_month(2019, 12), 31)
        self.assertEqual(days_in_month(2020, 2), 29)
