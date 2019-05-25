# -*- coding: utf-8 -*-
import json
from .models import Client, Rezept, Zutat, RezeptZutat, GangPlan
from .forms import ZutatForm, RezeptForm
from .utils import days_in_month, get_client, client_param
from datetime import date
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


MONAT = ("", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", 
         "August", "September", "Oktober", "November", "Dezember",)

def index(request):
    if get_client(request):
        # TODO: change to client's domain
        return redirect('/monat')
    return render(request, "rezepte/index.html")


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

@client_param
def rezepte(request, client_slug='', id=0, slug='', edit=False):
    if not (id or slug):
        # deliver all recipes
        recipes = Rezept.objects.filter(client__slug=client_slug)
        if len(recipes)==0:
            try:
                Client.objects.get(slug=client_slug)
            except Client.DoesNotExist:
                raise Http404
        return render(request, 'rezepte/rezepte.html', {'recipes': recipes})

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
            for rz in rezeptzutaten:
                RezeptZutat.objects.bulk_create(rezeptzutaten)
            return HttpResponseRedirect('/rezepte/' + recipe.slug)
    else:
        form = RezeptForm(instance=recipe)
    zutaten = Zutat.objects.filter(client__slug=client_slug)
    return render(request, 'rezepte/rezept-edit.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'rezeptzutaten': recipe.zutaten.all().select_related('zutat')})

@client_param
def zutaten(request, client_slug='', id=0):
    zutaten = Zutat.objects.filter(client__slug=client_slug
        ).order_by('kategorie', 'name')
    if id:
        zutat = zutaten.get(id=id)
        if not zutat:
            return Http404
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
            return HttpResponseRedirect('/zutaten/')
    else:
        form = ZutatForm(instance=zutat)
    return render(request, 'rezepte/zutaten.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'zutat_id': id or '',
                   'zutat': zutat,
                   'rezepte': rezepte})


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
        {'id': r.id, 'titel': r.titel,
         'kategorien': list(r.kategorie.names())}
        for r in Rezept.objects.filter(client__slug=client_slug)]
    data = {'planungen_js': json.dumps(planungen_js),
            'rezepte': json.dumps(rezepte),
            'month': month,
            'month_name': MONAT[month],
            'year': year,
            'gangfolge': "Vorspeise Hauptgang Nachtisch",
            'days_in_month': days_in_month(year, month)}
    return render(request, 'rezepte/monat.html', data)
