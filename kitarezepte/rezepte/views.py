# -*- coding: utf-8 -*-
import json
from .models import Client, Rezept, Zutat, GangPlan
from .forms import ZutatForm, RezeptForm
from .utils import days_in_month, get_client
from datetime import date
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


MONAT = ("", "Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", 
         "August", "September", "Oktober", "November", "Dezember",)

def index(request):
    if request.user.is_authenticated:
        # TODO: change to client's domain
        return redirect('/{}/monat'.format(request.session['client_slug']))
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


def rezepte(request, id=0, slug=''):
    client_slug = get_client(request)
    query_args = {'client__slug': client_slug}
    if id:
        query_args['id'] = int(id)
    elif slug:
        query_args['slug'] = slug
    else:
        # deliver all recipes
        recipes = Rezept.objects.filter(**query_args)
        if len(recipes)==0:
            # raise Http404 if client is not found
            get_object_or_404(Client, slug=client_slug)
        return render(request, 'rezepte/alle-rezepte.html', {'recipes': recipes})

    # just one recipe
    recipe = get_object_or_404(Rezept, **query_args)
    return render(request, 'rezepte/rezept.html', {'recipe': recipe})


def zutaten(request, id=0):
    client_slug = get_client(request)
    zutaten = Zutat.objects.filter(client__slug=client_slug
        ).order_by('kategorie', 'name')
    if id:
        zutat = zutaten.get(id=id)
    else:
        zutat = Zutat(client=Client.objects.get(slug=client_slug))
    if request.method == 'POST':
        form = ZutatForm(request.POST, instance=zutat)
        if form.is_valid():
            neue_zutat = form.save()
            return HttpResponseRedirect('')
    else:
        form = ZutatForm(instance=zutat)
    return render(request, 'rezepte/zutaten.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'zutat_id': id or ''})


def edit_rezept(request, client_slug, id=0):
    if request.method == 'POST':
        form = RezeptForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RezeptForm()

    return render(request, 'name.html', {'form': form})


def monat(request, year=0, month=0):
    client_slug = get_client(request)
    today = date.today()
    query_args = {'client__slug': client_slug}
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
        for r in Rezept.objects.filter(**query_args)]
    data = {'planungen_js': json.dumps(planungen_js),
            'rezepte': json.dumps(rezepte),
            'month': month,
            'month_name': MONAT[month],
            'year': year,
            'gangfolge': "Vorspeise Hauptgang Nachtisch",
            'days_in_month': days_in_month(year, month)}
    return render(request, 'rezepte/monat.html', data)
