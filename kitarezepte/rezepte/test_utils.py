# -*- coding: utf-8 -*-
from datetime import date
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, override_settings, RequestFactory
from .utils import (day_fromJson, prettyFloat, days_in_month,
                    euro2cent, next_dow, host2client, get_client)


class Host2ClientTestCase(TestCase):

    def test_host2client(self):

        def do_test(domain, expected):
            self.assertEqual(
                host2client(domain),
                expected,
                f"host2client liefert für {domain} {host2client(domain)} statt {expected}")

        do_test('localhost', 'dev')
        do_test('localhost:8000', 'dev')
        do_test('127.0.0.1', 'dev')
        do_test('127.0.0.1:8000', 'dev')
        do_test('testserver', 'test-kita')
        do_test('kita-rezepte.de', '')
        do_test('www.kita-rezepte.de', '')
        do_test(settings.KITAREZEPTE_FULL_DOMAIN, '')
        do_test('www.' + settings.KITAREZEPTE_FULL_DOMAIN, '')
        do_test('7zwerge.' + settings.KITAREZEPTE_FULL_DOMAIN, '7zwerge')

    @override_settings(ALLOWED_HOSTS=[
        "localhost", "testserver", ".kita-rezepte.de"])
    def test_get_client(self):
        factory = RequestFactory()
        request = factory.get('/')
        anonymous = AnonymousUser()
        user = User.objects.create_user(
            username='jammon', email='j@j.de', password='password')

        def do_test(domain, authenticated, expected):
            request.META['HTTP_HOST'] = domain
            request.user = user if authenticated else anonymous
            result = get_client(request)
            self.assertEqual(
                result,
                expected,
                f"get_client liefert für {domain} "
                f"{'(angemeldet) ' if authenticated else ''}"
                f"{result} statt {expected}")

        do_test('localhost', True, 'dev')
        do_test('localhost', False, '')
        do_test('7zwerge.kita-rezepte.de', True, '7zwerge')
        do_test('7zwerge.kita-rezepte.de', False, '7zwerge')


class Day_fromJsonTestCase(TestCase):

    def test_day_fromJson(self):
        """ Strings are translated to Dates """
        self.assertEqual(day_fromJson("2019-03-22"), date(2019, 3, 22))
        self.assertEqual(day_fromJson("2019-01-01"), date(2019, 1, 1))
        self.assertEqual(day_fromJson("2019-12-31"), date(2019, 12, 31))


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


class Euro2CentTestCase(TestCase):

    def test_euro2cent(self):
        """ Calculates the Cents from an Euro string """
        self.assertEqual(euro2cent("15"), 1500)
        self.assertEqual(euro2cent("3,79"), 379)
        self.assertEqual(euro2cent("3.79"), 379)
        self.assertRaises(ValueError, euro2cent, "foo")
        self.assertRaises(ValueError, euro2cent, "3,79 Euro")


class Next_DowTestCase(TestCase):

    def test_next_dow(self):
        """ Calculates the next occurence of a certain day of week """
        today = date(2019, 5, 30)  # Thursday = 3
        self.assertEqual(next_dow(3, today), today)
        self.assertEqual(next_dow(4, today), date(2019, 5, 31))
        self.assertEqual(next_dow(6, today), date(2019, 6, 2))
        self.assertEqual(next_dow(0, today), date(2019, 6, 3))
        self.assertEqual(next_dow(2, today), date(2019, 6, 5))
