# -*- coding: utf-8 -*-
import json
from .models import (Client, Rezept, Zutat, RezeptZutat, GangPlan,
                     get_einkaufsliste)
from .forms import ZutatForm, RezeptForm
from .utils import (check_client, days_in_month, next_dow,
                    MONATSNAMEN, next_month)
from datetime import date
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import select_template


def index(request):
    if request.client is not None:
        return render(
            request, "rezepte/client-index.html",
            {'client': request.client,
             'template': select_template(
                [f'rezepte/clients/{c}.html' for c in
                 (request.client.slug, 'generic')]),
             'no_login_link': True})
    clients = Client.objects.all().order_by('name')
    return render(request, "rezepte/index.html",
                  {'clients': clients, 'no_login_link': True})


# TODO: Wie mit request.client umgehen?
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                write_client_id_to_session(request.session, user)
                client_slug = request.session.get('client_slug')
                if client_slug:
                    if client_slug == "dev":
                        return HttpResponseRedirect('/monat')
                    return HttpResponseRedirect(
                        f'https://{client_slug}.'
                        f'{settings.KITAREZEPTE_FULL_DOMAIN}/monat')
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Fehler bei der Anmeldung!")
    else:
        form = AuthenticationForm()
    return render(request, 'rezepte/login.html', {'form': form})


# TODO: Wie mit request.client umgehen?
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def write_client_id_to_session(session, user):
    session['user_name'] = user.get_full_name() or user.get_username()
    try:
        client = user.editor.client
        session['client_id'] = client.id
        session['client_slug'] = client.slug
        session['gaenge'] = client.get_gaenge()
        session['kategorien'] = client.get_kategorien()
    except auth.models.User.editor.RelatedObjectDoesNotExist:
        pass


# TODO: Wie mit request.client umgehen?
def get_query_args(id=0, slug=''):
    res = {}
    if id:
        res['id'] = int(id)
    elif slug:
        res['slug'] = slug
    return res


# Rezepte ------------------------------------------------------------------
def rezepte(request, id=0, slug=''):
    if not (id or slug):
        # deliver all recipes
        return alle_rezepte(request)

    # show just one recipe
    try:
        rezept = Rezept.objects.get(
            client=request.client,
            **get_query_args(id, slug))
    except Rezept.DoesNotExist:
        return alle_rezepte(
            request,
            msg=f"Rezept \"{slug or id}\" nicht gefunden")
    return render(
        request,
        'rezepte/rezept.html',
        {'recipe': rezept,
         'zutaten': rezept.zutaten.all().select_related('zutat')
            .order_by('nummer')})


def alle_rezepte(request, msg=''):
    """ Zeigt alle Rezepte, für jeden Gang eine Spalte,
        dann nach Kategorien geordnet
    """
    if request.client is None:
        raise Http404
    recipes = Rezept.objects.filter(client=request.client).order_by('slug')
    gaenge = request.client.get_gaenge()
    kategorien = request.client.get_kategorien()
    data = []
    for g in gaenge:
        g_data = []
        for k in kategorien:
            k_data = []
            for r in recipes:
                if g in r.gang and k in r.kategorien:
                    k_data.append(r)
            # k_data = [r for r in recipes
            #           if g in r.gang and k in r.kategorien]
            if k_data:
                g_data.append((k, k_data))
        # keine Kategorie
        k_data = [r for r in recipes
                  if g in r.gang and r.kategorien.strip() == ""]
        if k_data:
            g_data.append(("keine Kategorie", k_data))
        if g_data:
            data.append((g, g_data))
    return render(
        request, 'rezepte/rezepte.html', {
            'recipes': data,
            'msg': msg
        })


@login_required
@check_client
def rezept_edit(request, id=0, slug=''):
    if id or slug:
        rezept = get_object_or_404(
            Rezept, client=request.client, **get_query_args(id, slug))
    else:
        # neues Rezept
        rezept = Rezept(client=request.client)
    if request.method == 'POST':
        form = RezeptForm(
            request.POST, instance=rezept, session=request.session)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            rezept = form.save()
            # ditch old RezeptZutaten
            RezeptZutat.objects.filter(rezept=rezept).delete()
            # collect and save RezeptZutaten
            rezeptzutaten = [
                RezeptZutat(rezept=rezept, **json.loads(v))
                for k, v in request.POST.items() if k.startswith('rz')]
            RezeptZutat.objects.bulk_create(rezeptzutaten)
            return HttpResponseRedirect('/rezepte/' + rezept.slug)
    else:
        form = RezeptForm(instance=rezept, session=request.session)
    zutaten = Zutat.objects.filter(client=request.client)
    rezeptzutaten = (
        rezept.zutaten.all().select_related('zutat')
        if rezept is not None else [])
    return render(request, 'rezepte/rezept-edit.html',
                  {'form': form,
                   'zutaten': zutaten,
                   'zutatenform': ZutatForm(),
                   'rezeptzutaten': rezeptzutaten})


# Zutaten ------------------------------------------------------------------
@login_required
def zutaten(request, msg=''):
    zutaten = Zutat.objects.filter(
        client=request.client
    ).annotate(Count('rezepte')).order_by('kategorie', 'name')
    return render(request, 'rezepte/zutaten.html',
                  {'zutaten': zutaten,
                   'msg': msg})


@login_required
@check_client
def zutat_edit(request, id=0, msg=''):
    if id:
        try:
            zutat = Zutat.objects.get(
                id=id, client_id=request.session['client_id'])
        except Zutat.DoesNotExist:
            raise Http404
        rezepte = Rezept.objects.filter(
            zutaten__zutat=zutat
        ).order_by('titel')
    else:
        # neue Zutat
        zutat = Zutat(client=request.client)
        rezepte = []
    if request.method == 'POST':
        form = ZutatForm(request.POST, instance=zutat)
        if form.is_valid():
            neue_zutat = form.save()
            neue_zutat.updateRezeptpreise()
            return HttpResponseRedirect('/zutaten/')
    else:
        form = ZutatForm(instance=zutat)
    return render(request, 'rezepte/zutat-edit.html',
                  {'form': form,
                   'zutat_id': id or '',
                   'zutat': zutat,
                   'rezepte': rezepte})


@login_required
@check_client
def zutaten_delete(request):
    if request.method != 'POST' or 'zutat_id' not in request.POST:
        return redirect("zutaten")
    id = request.POST['zutat_id']
    zutat = get_object_or_404(Zutat, client=request.client, id=id)
    # TODO: check for recipes
    zutat.delete()
    return redirect("/zutaten/",
                    msg=f'Zutat {zutat.name} wurde gelöscht')


# Monat ------------------------------------------------------------------
def monat(request, year=0, month=0):
    today = date.today()
    year = int(year) or today.year
    month = int(month) or today.month
    if month == 12:
        naechster_erster = date(year+1, 1, 1)
    else:
        naechster_erster = date(year, month+1, 1)
    planungen = GangPlan.objects.filter(
        datum__gte=date(year, month, 1),
        datum__lt=naechster_erster,
        client=request.client,
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
         'preis': str(r.preis() or '--').replace('.', ',')}
        for r in Rezept.objects.filter(
                client=request.client
            ).order_by('slug')]
    data = {'planungen': planungen_js,
            'rezepte': rezepte,
            'month': month,
            'year': year,
            'gangfolge': request.client.gaenge,
            'days_in_month': days_in_month(year, month),
            'is_authenticated': request.user.is_authenticated}
    gaenge = request.client.gaenge.split()
    return render(request, 'rezepte/monat.html', {
        'data': json.dumps(data),
        'month_name': MONATSNAMEN[month],
        'year': year,
        'next': next_month(year, month, 1),
        'prev': next_month(year, month, -1),
        'gaenge': gaenge,
        'gangbreite': 12 // len(gaenge),
    })


# Tag ------------------------------------------------------------------
def tag(request, year=0, month=0, day=0):
    day = date(int(year), int(month), int(day)) if year else date.today()
    planungen = GangPlan.objects.filter(
        datum=day,
        client=request.client,
    ).select_related('rezept')

    def sortkey(planung):
        return request.client.gaenge.find(planung.gang)

    data = {'planungen': sorted(planungen, key=sortkey),
            'day': day,
            'is_authenticated': request.user.is_authenticated}
    return render(request, 'rezepte/tag.html', data)


# Einkaufsliste ---------------------------------------------------------------
def einkaufsliste(request, year=0, month=0, day=0, dauer=7):
    msg = ""
    try:
        start = date(year, month, day)
    except ValueError:
        if year != 0:
            msg = f'"{day}.{month}.{year}" ist keine Datumsangabe.'
        start = next_dow(0)
    data = get_einkaufsliste(request.client, start, dauer)
    data["msg"] = msg
    return render(request, 'rezepte/einkaufsliste.html', data)
