# coding: utf-8
from datetime import date, timedelta
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from functools import wraps


MONATSNAMEN = ("", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
               "August", "September", "Oktober", "November", "Dezember",)


def get_provider_domain(slug):
    if slug in ('dev', 'test-kita'):
        return '127.0.0.1:8000'
    return slug + '.' + settings.KITAREZEPTE_FULL_DOMAIN


def check_client(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.client.slug != request.session.get('client_slug'):
            return HttpResponse(status=403, reason="Falscher Client.")
        return f(request, *args, **kwargs)
    return wrapper


def check_provider(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.provider.slug != request.session.get('provider_slug'):
            return HttpResponse(status=403, reason="Falsche Einrichtung.")
        return f(request, *args, **kwargs)
    return wrapper


def day_fromJson(day):
    """ expects a string like '2019-04-23' """
    return date(int(day[0:4]), int(day[5:7]), int(day[8:10]))


def days_in_month(year, month):
    """ number of days in a given month

    Is correct 1901 to 2099.
    """
    if month == 2 and year % 4 == 0:
        return 29
    return (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month-1]


def prettyFloat(f):
    s = str(f).replace('.', ',')
    return s[:-2] if s.endswith(u',0') else s


def cent2euro(cent):
    return f"{cent / 100.0:.2f}".replace('.', ',')


def euro2cent(euro):
    """ Calculates the Cents from an Euro string.

    Can raise ValueError
    """
    return int(round(100*float(euro.replace(',', '.'))))


def next_dow(dow, today=None):
    """ return next <day of week> as date

    where <day of week> is 0..6 for Monday..Sunday.
    The <today> argument is only for testing
    """
    today = today or date.today()
    weekday = today.weekday()
    return today + timedelta(
        days=dow - weekday + (0 if weekday <= dow else 7))


def next_month(year, month, offset=1):
    newyear, newmonth = year, month + offset
    if newmonth < 1:
        newmonth += 12
        newyear += -1
    elif newmonth > 12:
        newmonth += -12
        newyear += 1
    return {
        'name': f"{MONATSNAMEN[newmonth]} {newyear}",
        'link': f"/monat/{newyear}/{newmonth}",
    }


TEST_REIS = dict(name="Reis",
                 einheit="1 kg",
                 preis=Decimal('1.89'),
                 menge_pro_einheit=1000,
                 masseinheit="g",
                 kategorie="Grundnahrungsmittel")

TEST_REZEPT = dict(
            fuer_kinder=20,
            fuer_erwachsene=5,
            zubereitung='',
            anmerkungen='',
            gang='Hauptgang',
            kategorien='')
