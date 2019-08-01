# coding: utf-8
from datetime import date, timedelta
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404


MONATSNAMEN = ("", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", 
         "August", "September", "Oktober", "November", "Dezember",)

def get_client(request):
    return host2client(get_current_site(request).domain)

def host2client(host):
    h = host.split(':')[0].split('.')[0]
    if h in ('localhost', '127'):
        return 'dev'
    if h == 'testserver':
        # for unittests
        return 'test-kita'
    if h in ('kita-rezepte', settings.KITAREZEPTE_DOMAIN, 'www'):
        return ''
    return h

def get_client_domain(slug):
    if slug in ('dev', 'test-kita'):
        return '127.0.0.1'
    return slug + '.' + settings.KITAREZEPTE_FULL_DOMAIN


def client_param(view):
    def view_with_client_param(request, *args, **kwargs):
        client_slug = get_client(request)
        if not client_slug:
            raise Http404
        return view(request, client_slug, *args, **kwargs)
    return view_with_client_param

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
    s = str(f)
    return s[:-2] if s.endswith(u'.0') else s

def cent2euro(cent):
    res = "{:.2f}".format(cent / 100.0)
    return res.replace('.', ',')

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
        days = dow - weekday + (0 if weekday<=dow else 7))

def next_month(year, month, offset=1):
    newyear, newmonth = year, month + offset
    if newmonth<1:
        newmonth += 12
        newyear += -1
    elif newmonth>12:
        newmonth += -12
        newyear += 1
    return {
        'name': "{} {}".format(MONATSNAMEN[newmonth], newyear),
        'link': "/monat/{}/{}".format(newyear, newmonth),
    }


TEST_REIS = dict(name="Reis", 
            client_id = 1,
            einheit="1 kg",
            preis_pro_einheit=189,
            menge_pro_einheit=1000,
            masseinheit="g",
            kategorie="Grund.")

TEST_REZEPT = dict(
            client_id = 1,
            fuer_kinder = 20,
            fuer_erwachsene = 5,
            zubereitung = '',
            anmerkungen = '',
            kategorie = '')

