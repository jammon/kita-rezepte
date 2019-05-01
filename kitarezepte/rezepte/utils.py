# coding: utf-8
from datetime import date
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404


def get_client(request):
    current_site = get_current_site(request)
    client = current_site.domain.split('.')[0]
    if client in ('localhost', '127'):
        return 'dev' if request.user.is_authenticated else ''
    if client == 'testserver':
        return 'test-kita'
    if client == 'kita-rezepte':
        return ''
    return client

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

