# -*- coding: utf-8 -*-
import json
from .models import (Client, Rezept, Zutat, RezeptZutat, GangPlan, KEIN_PREIS,
                     get_einkaufsliste)
from .forms import ZutatForm, RezeptForm
from .utils import (days_in_month, get_client, client_param, next_dow, MONATSNAMEN, 
                    next_month)
from datetime import date, timedelta
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


def index(request):
    client_slug = get_client(request)
    print('client_slug:', client_slug)
    if client_slug:
        client = get_object_or_404(Client, slug=client_slug)
        return render(request, "rezepte/client-index.html", {'client': client})
    clients = Client.objects.all().order_by('name')
    return render(request, "rezepte/index.html", {'clients': clients})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                write_client_id_to_session(request.session, user)
                if request.session['client_slug']:
                    # TODO: change to client's domain
                    return HttpResponseRedirect('/monat')
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Fehler bei der Anmeldung!")
    else:
        form = AuthenticationForm()
    return render(request, 'rezepte/login.html', {'form': form})


def write_client_id_to_session(session, user):
    session['user_name'] = user.get_full_name() or user.get_username()
    if user.editor:
        client = user.editor.client
        session['client_id'] = client.id
        session['client_slug'] = client.slug
        session['gaenge'] = client.get_gaenge()
        session['kategorien'] = client.get_kategorien()


def get_query_args(client_slug='', id=0, slug=''):
    res =  {'client__slug': client_slug}
    if id:
        res['id'] = int(id)
    elif slug:
        res['slug'] = slug
    return res


# Rezepte ------------------------------------------------------------------
@client_param
def rezepte(request, client_slug='', id=0, slug='', edit=False):
    if not (id or slug):
        # deliver all recipes
        recipes = Rezept.objects.filter(client__slug=client_slug).order_by('slug')
        client = get_object_or_404(Client, slug=client_slug)
        gaenge = client.gaenge.split()
        data = [(g, [r for r in recipes if g in r.gang]) for g in gaenge]
        data.append(("unsortiert", [r for r in recipes if r.gang.strip()=='']))
        return render(request, 'rezepte/rezepte.html', {'recipes': data})

    if edit:
        return rezept_edit(request, client_slug, id, slug)

    # show just one recipe
    rezept = get_object_or_404(Rezept, **get_query_args(client_slug, id, slug))
    return render(
        request,
        'rezepte/rezept.html',
        {'recipe': rezept,
         'zutaten': rezept.zutaten.all().select_related('zutat').order_by('nummer')})

def rezept_edit(request, client_slug, id, slug):
    if id or slug:
        rezept = get_object_or_404(Rezept, **get_query_args(client_slug, id, slug))
    else:
        rezept = None
    if request.method == 'POST':
        form = RezeptForm(request.POST, instance=rezept, session=request.session)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            form.save()
            # ditch old RezeptZutaten
            RezeptZutat.objects.filter(rezept=rezept).delete()
            # collect and save RezeptZutaten
            rezeptzutaten = []
            for k, v in request.POST.items():
                if k.startswith('rz'):
                    rezeptzutaten.append(RezeptZutat(rezept=rezept, **json.loads(v)))
            RezeptZutat.objects.bulk_create(rezeptzutaten)
            return HttpResponseRedirect('/rezepte/' + rezept.slug)
    else:
        form = RezeptForm(instance=rezept, session=request.session)
    zutaten = Zutat.objects.filter(client__slug=client_slug)
    return render(request, 'rezepte/rezept-edit.html', 
                  {'form': form,
                   'zutaten': zutaten,
                   'rezeptzutaten': rezept.zutaten.all().select_related('zutat')})


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
                    msg=f'Zutat {zutat.name} wurde gelöscht')


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
         'gang': r.gang.split(),
         'kategorien': r.kategorie_list,
         'preis': '--' if r._preis==KEIN_PREIS else r._preis}
        for r in Rezept.objects
            .filter(client__slug=client_slug)
            .order_by('slug')]
    client = get_object_or_404(Client, slug=client_slug)
    data = {'planungen': planungen_js,
            'rezepte': rezepte,
            'month': month,
            'year': year,
            'gangfolge': client.gaenge,
            'days_in_month': days_in_month(year, month),
            'is_authenticated': request.user.is_authenticated }
    return render(request, 'rezepte/monat.html', {
        'data': json.dumps(data),
        'month_name': MONATSNAMEN[month],
        'year': year,
        'next': next_month(year, month, 1),
        'prev': next_month(year, month, -1),
    })


# Tag ------------------------------------------------------------------
@client_param
def tag(request, client_slug, year=0, month=0, day=0):
    day = date(int(year), int(month), int(day)) if year else date.today()
    planungen = GangPlan.objects.filter(
        datum=day,
        client__slug=client_slug,
    ).select_related('rezept')
    client = get_object_or_404(Client, slug=client_slug)
    def sortkey(planung):
        return client.gaenge.find(planung.gang)
    data = {'planungen': sorted(planungen, key=sortkey),
            'day': day,
            'is_authenticated': request.user.is_authenticated }
    return render(request, 'rezepte/tag.html', data)


# Einkaufsliste ------------------------------------------------------------------
@client_param
def einkaufsliste(request, client_slug, start=None, dauer=0):
    start = start or next_dow(1)  # TODO: auf den einzelnen Client anpassen
    dauer = dauer or 7
    return render(request, 'rezepte/einkaufsliste.html',
                  get_einkaufsliste(client_slug, start, dauer))
