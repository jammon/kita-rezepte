# coding: utf-8
from datetime import date
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import Http404


def _client_kwargs(client_id='', client_slug='', **kwargs):
    _kwargs = kwargs.copy()
    if client_id:
        _kwargs['client__id'] = client_id
    elif client_slug:
        _kwargs['client__slug'] = client_slug
    else:
        raise Http404("Either client_id or client_slug have to be given")
    return _kwargs

def get_for_client(
        klass, client_id='', client_slug='', **kwargs):
    return get_object_or_404(
        klass, _client_kwargs(client_id, client_slug, **kwargs))

def get_list_for_client(
        klass, client_id='', client_slug='', **kwargs):
    return get_list_or_404(
        klass, _client_kwargs(client_id, client_slug, **kwargs))


def str2date(s):
    res = s.split('.')
    res.reverse()
    return date(*[int(n) for n in res])

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

