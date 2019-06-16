# -*- coding: utf-8 -*-
import json
from .models import (Client, Rezept, Zutat, RezeptZutat, GangPlan, KEIN_PREIS,
                     get_einkaufsliste)
from .forms import ZutatForm, RezeptForm
from .utils import (days_in_month, get_client, client_param, next_dow, MONATSNAMEN, 
                    next_month)
from datetime import date, timedelta
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


def index(request):
    client_slug = get_client(request)
    if client_slug:
        client = get_object_or_404(Client, slug=client_slug)
        return render(request, "rezepte/client-index.html", {'client': client})
    clients = Client.objects.all().order_by('name')
    return render(request, "rezepte/index.html", {'clients': clients})


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AuthenticationForm(request, request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                request.session['user_name'] = user.get_full_name() or user.get_username()
                client = user.editor.client
                if client:
                    request.session['client_slug'] = client.slug
                    # TODO: change to client's domain
                    return HttpResponseRedirect('/monat')
                # redirect to a new URL:
                return HttpResponseRedirect('/')
            else:
                # Return an 'invalid login' error message.
                form.add_error(None, "Fehler bei der Anmeldung!")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AuthenticationForm()

    return render(request, 'rezepte/login.html', {'form': form})

def get_query_args(client_slug='', id=0, slug=''):
    if id:
        return {'client__slug': client_slug, 'id': int(id)}
    if slug:
        return {'client__slug': client_slug, 'slug': slug}
    return {'client__slug': client_slug}


# Rezepte ------------------------------------------------------------------
@client_param
def rezepte(request, client_slug='', id=0, slug='', edit=False):
    if not (id or slug):
        # deliver all recipes
        recipes = Rezept.objects.filter(client__slug=client_slug)
        client = get_object_or_404(Client, slug=client_slug)
        gaenge = client.gaenge.split()
        for r in recipes:
            for g in gaenge:
                if g in r.kategorie.names():
                    r.gang = g
                    break
            else:
                r.gang = 'Unsortiert'
        def sortkey(rezept):
            return rezept.gang + rezept.slug
        return render(request, 'rezepte/rezepte.html',
                      {'recipes': sorted(recipes, key=sortkey)})

    if edit:
        return rezept_edit(request, client_slug, id, slug)

    # show just one recipe
    recipe = get_object_or_404(Rezept, **get_query_args(client_slug, id, slug))
    return render(
        request,
        'rezepte/rezept.html',
        {'recipe': recipe,
         'zutaten': recipe.zutaten.all().select_related('zutat')})

def rezept_edit(request, client_slug, id, slug):
    if id or slug:
        recipe = get_object_or_404(Rezept, **get_query_args(client_slug, id, slug))
    else:
        recipe = None
    if request.method == 'POST':
        form = RezeptForm(request.POST, instance=recipe)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            # ditch old RezeptZutaten
            RezeptZutat.objects.filter(rezept=recipe).delete()
            # collect and save RezeptZutaten
            rezeptzutaten = []
            for k, v in request.POST.items():
                if k.startswith('rz'):
                    rezeptzutaten.append(RezeptZutat(rezept=recipe, **json.loads(v)))
            RezeptZutat.objects.bulk_create(rezeptzutaten)
            return HttpResponseRedirect('/rezepte/' + recipe.slug)
    else:
        form = RezeptForm(instance=recipe)
    zutaten = Zutat.objects.filter(client__slug=client_slug)
    return render(request, 'rezepte/rezept-edit.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'rezeptzutaten': recipe.zutaten.all().select_related('zutat')})


# Zutaten ------------------------------------------------------------------
@login_required
@client_param
def zutaten(request, client_slug='', id=0, msg=''):
    zutaten = Zutat.objects.filter(client__slug=client_slug
        ).order_by('kategorie', 'name')
    if id:
        try:
            zutat = zutaten.get(id=id)
        except Zutat.DoesNotExist:
            raise Http404
        rezepte = Rezept.objects.filter(zutaten__zutat=zutat
            ).order_by('titel')
    else:
        # neue Zutat
        zutat = Zutat(client=Client.objects.get(slug=client_slug))
        rezepte = []
    if request.method == 'POST':
        form = ZutatForm(request.POST, instance=zutat)
        if form.is_valid():
            neue_zutat = form.save()
            neue_zutat.updateRezeptpreise()
            return HttpResponseRedirect('/zutaten/')
    else:
        form = ZutatForm(instance=zutat)
    print('msg: ', msg)
    return render(request, 'rezepte/zutaten.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'zutat_id': id or '',
                   'zutat': zutat,
                   'rezepte': rezepte,
                   'msg': msg,
                   'is_authenticated': request.user.is_authenticated })


@client_param
def zutaten_delete(request, client_slug=''):
    if request.method != 'POST' or 'zutat_id' not in request.POST:
        return redirect("zutaten")
    id = request.POST['zutat_id']
    zutat = get_object_or_404(Zutat, client__slug=client_slug, id=id)
    Zutat.objects.filter(client__slug=client_slug, id=id).delete()
    return redirect("/zutaten/", 
                    client_slug=client_slug,
                    msg='Zutat {} wurde gelöscht'.format(zutat.name))


# Monat ------------------------------------------------------------------
@client_param
def monat(request, client_slug, year=0, month=0):
    today = date.today()
    year = int(year) or today.year
    month = int(month) or today.month
    if month==12:
        naechster_erster = date(year+1, 1, 1)
    else:
        naechster_erster = date(year, month+1, 1)
    planungen = GangPlan.objects.filter(
        datum__gte=date(year, month, 1),
        datum__lt=naechster_erster,
        client__slug=client_slug,
    ).select_related('rezept')
    planungen_js = [
        {'datum': [g.datum.year, g.datum.month, g.datum.day],
         'gang': g.gang, 
         'rezept_id': g.rezept.id, 
         'rezept_titel': g.rezept.titel} for g in planungen]
    rezepte = [
        {'id': r.id, 
         'titel': r.titel,
         'kategorien': list(r.kategorie.names()),
         'preis': '--' if r._preis==KEIN_PREIS else r._preis}
        for r in Rezept.objects.filter(client__slug=client_slug)]
    data = {'planungen': planungen_js,
            'rezepte': rezepte,
            'month': month,
            'year': year,
            'gangfolge': "Vorspeise Hauptgang Nachtisch",
            'days_in_month': days_in_month(year, month),
            'is_authenticated': request.user.is_authenticated }
    return render(request, 'rezepte/monat.html', {
        'data': json.dumps(data),
        'month_name': MONATSNAMEN[month],
        'year': year,
        'next': next_month(year, month, 1),
        'prev': next_month(year, month, -1),
    })

# Einkaufsliste ------------------------------------------------------------------
@client_param
def einkaufsliste(request, client_slug, start=None, dauer=0):
    start = start or next_dow(1)  # TODO: auf den einzelnen Client anpassen
    dauer = dauer or 7
    return render(request, 'rezepte/einkaufsliste.html',
                  get_einkaufsliste(client_slug, start, dauer))
