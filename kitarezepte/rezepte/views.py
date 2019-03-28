import json
from datetime import date
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Rezept, Zutat, Menue
from .utils import days_in_month

MONAT = ("", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", 
         "August", "September", "Oktober", "November", "Dezember",)

def index(request):
    if request.user.is_authenticated:
        return redirect('monat')
    return render(request, "rezepte/index.html")

def login(request):
    return "login"


def get_client_query_args(client_id='', client_slug=''):
    """ Query arguments for client """
    query_args = {}
    if client_id:
        query_args['client__id'] = client_id
    if client_slug:
        query_args['client__slug'] = client_slug
    return query_args

def rezepte(request, client_id='', client_slug='', id=0, slug=''):
    data = {'client': client_id or client_slug}
    query_args = get_client_query_args(client_id, client_slug)
    if id:
        query_args['id'] = int(id)
    elif slug:
        query_args['slug'] = slug
    else:
        # deliver all recipes
        data['recipes'] = get_list_or_404(Rezept, **query_args)
        return render(request, 'rezepte/alle-rezepte.html', data)

    # just one recipe
    data['recipe'] = get_object_or_404(Rezept, **query_args)
    return render(request, 'rezepte/ein-rezept.html', data)

def zutaten(request, client_id='', client_slug='', id=0):
    data = {'client': client_id or client_slug}
    query_args = get_client_query_args(client_id, client_slug)
    data['zutaten'] = get_list_or_404(Zutat, **query_args)
    return render(request, 'rezepte/zutaten.html', data)

def menu_array(day, menu):
    if menu is None:
        return [day, [0, ''], [0, ''], [0, '']]
    res = [day]
    for g in ("vorspeise", "hauptgang", "nachtisch"):
        rezept = getattr(menu, g)
        res.append(
            [0, ''] if rezept is None else
            [rezept.id, rezept.titel])
    return res

def monat(request, client_id='', client_slug='', year=0, month=0):
    today = date.today()
    query_args = get_client_query_args(client_id, client_slug)
    year = int(year) or today.year
    month = int(month) or today.month
    if month==12:
        naechster_erster = date(year+1, 1, 1)
    else:
        naechster_erster = date(year, month+1, 1)
    menues = Menue.objects.filter(
        datum__gte=date(year, month, 1),
        datum__lt=naechster_erster,
        **query_args
    ).select_related('vorspeise', 'hauptgang', 'nachtisch')
    days = [None, ] * days_in_month(year, month)
    for menu in menues:
        days[menu.datum.day-1] = menu
    days_js = [menu_array(day, menu) for day, menu in enumerate(days, start=1)]
    rezepte = [
        {'id': r.id, 'titel': r.titel,
         'kategorien': list(r.kategorie.names())}
        for r in Rezept.objects.filter(**query_args)]
    data = {'days': days,
            'days_js': json.dumps(days_js),
            'rezepte': json.dumps(rezepte),
            'month': month,
            'month_name': MONAT[month],
            'year': year}
    return render(request, 'rezepte/monat.html', data)
