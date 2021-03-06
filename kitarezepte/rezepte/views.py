# -*- coding: utf-8 -*-
import json
from datetime import date

from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import select_template

from .forms import ZutatForm, RezeptForm
from .models import (Client, Provider, Rezept, Zutat, RezeptZutat,
                     GangPlan, get_einkaufsliste, Editor)
from .utils import (check_client, check_provider, days_in_month, next_dow,
                    MONATSNAMEN, next_month)


def index(request):
    if request.provider is not None:
        return render(
            request, "rezepte/provider-index.html",
            {'provider': request.provider,
             'template': select_template(
                [f'rezepte/providers/{c}.html' for c in
                 (request.provider.slug, 'generic')]),
             'no_login_link': True})
    providers = Provider.objects.all().order_by('name')
    return render(request, "rezepte/index.html",
                  {'providers': providers, 'no_login_link': True})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                session = request.session
                session['user_name'] = user.get_full_name() or user.get_username()
                # get client for user
                try:
                    client = user.editor.client
                except (Editor.DoesNotExist, Client.DoesNotExist):
                    # The user is not editor of a client
                    # TODO: Add some message?
                    return redirect('/')
                # get providers for client
                providers = client.providers.all()
                if len(providers) == 1:
                    # it's only one -> use it
                    return redirect(
                        f'{providers[0].full_path()}/choose_provider')
                elif len(providers) == 0:
                    # there is no provider
                    return redirect('/')
                    # TODO: Add some message? Should not happen!
                else:
                    # present choice
                    return redirect("providers")
            else:
                form.add_error(None, "Fehler bei der Anmeldung!")
    else:
        form = AuthenticationForm()
    return render(request, 'rezepte/login.html', {'form': form})


def write_provider_to_session(request, providers=None):
    # is a separate function for testing
    provider = request.provider
    request.session['client_id'] = provider.client.id
    request.session['client_slug'] = provider.client.slug
    request.session['provider_id'] = provider.id
    request.session['provider_slug'] = provider.slug
    request.session['provider_name'] = provider.name
    request.session['provider_path'] = provider.full_path()
    request.session['gaenge'] = provider.get_gaenge()
    request.session['kategorien'] = provider.get_kategorien()
    if providers is None:
        providers = provider.client.providers.all()
    if len(providers) > 1:
        request.session['other_providers'] = tuple(
            (p.name, p.full_path()) for p in providers if p.id != provider.id)


@login_required
def providers(request):
    return render(
        request, 'rezepte/providers.html',
        {'providers': request.user.editor.client.providers.all()})


@login_required
def choose_provider(request):
    provider = request.provider
    if provider and provider.client_id == request.user.editor.client_id:
        write_provider_to_session(request)
        return redirect('/monat')
    else:
        # TODO: error message;  Should not happen!
        return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('/')


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
            provider=request.provider,  # TODO: brauche ich die Zeile?
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
            .order_by('nummer'),
         'user_is_editor':
            request.provider.id == request.session.get('provider_id')})


def alle_rezepte(request, msg=''):
    """ Zeigt alle Rezepte, für jeden Gang eine Spalte,
        dann nach Kategorien geordnet
    """
    if request.provider is None:
        raise Http404  # TODO: Redirect auf Hauptseite
    all_recipes = Rezept.objects.filter(provider=request.provider).order_by('slug')
    recipes = [r for r in all_recipes if r.aktiv]
    gaenge = request.provider.get_gaenge()
    kategorien = request.provider.get_kategorien()
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
            'inaktive': [r for r in all_recipes if not r.aktiv],
            'msg': msg,
        })


@login_required
@check_provider
def rezept_edit(request, id=0, slug=''):
    if id or slug:
        rezept = get_object_or_404(
            Rezept, provider=request.provider, **get_query_args(id, slug))
    else:
        # neues Rezept
        rezept = Rezept(provider=request.provider)
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


@login_required
def rezept_takeover(request, id):
    original = get_object_or_404(Rezept, id=id)
    if original.provider_id == request.session['provider_id']:
        return redirect('/rezepte/')
    gaenge = ' '.join(
        g for g in original.gang_list
        if g in request.session['gaenge'])
    kategorien = ' '.join(
        k for k in original.kategorie_list
        if k in request.session['kategorien'])
    rez = Rezept.objects.create(
        titel=original.titel,
        untertitel=original.untertitel,
        client_id=request.session['client_id'],
        provider_id=request.session['provider_id'],
        slug=original.slug,
        fuer_kinder=original.fuer_kinder,
        fuer_erwachsene=original.fuer_erwachsene,
        zubereitung=original.zubereitung,
        anmerkungen=original.anmerkungen,
        gang=gaenge,
        kategorien=kategorien,
    )
    zutaten = original.zutaten.all().select_related('zutat')
    z_dict = dict((zutat.name, zutat) for zutat in Zutat.objects.filter(
        name__in=(z.zutat.name for z in zutaten)))
    rz = []
    for z in zutaten:
        rz.append(RezeptZutat(
            rezept=rez,
            zutat=z_dict.get(z.zutat.name) or Zutat.objects.create(
                name=z.zutat.name,
                client=request.client,
                einheit=z.zutat.einheit,
                menge_pro_einheit=z.zutat.menge_pro_einheit,
                masseinheit=z.zutat.masseinheit,
                kategorie=z.zutat.kategorie),
            menge=z.menge,
            menge_qualitativ=z.menge_qualitativ,
            nummer=z.nummer))
    RezeptZutat.objects.bulk_create(rz)
    return redirect(rez)


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
        ).order_by('provider__name', 'titel').select_related('provider')
    else:
        # neue Zutat
        zutat = Zutat(client=request.client)
        rezepte = []
    if request.method == 'POST':
        form = ZutatForm(request.POST, instance=zutat)
        if form.is_valid():
            neue_zutat = form.save(commit=False)
            neue_zutat.allergene = ''.join(
                val for key, val in request.POST.items()
                if key.startswith('allergen_'))
            neue_zutat.save()
            neue_zutat.updateRezepte()
            return HttpResponseRedirect('/zutaten/')
    else:
        form = ZutatForm(instance=zutat)
    return render(request, 'rezepte/zutat-edit.html',
                  {'form': form,
                   'zutat_id': id or '',
                   'zutat': zutat,
                   'rezepte': rezepte,
                   'allergene': Zutat.ALLERGENE})


@login_required
@check_client
def zutaten_delete(request):
    if request.method != 'POST' or 'zutat_id' not in request.POST:
        return redirect("zutaten")
    id = request.POST['zutat_id']
    try:
        zutat = Zutat.objects.get(client=request.client, id=id)
    except Zutat.DoesNotExist:
        return redirect("/zutaten/",
                        msg='Fehler beim Löschen einer Zutat')
    rezepte = list(zutat.rezepte.values_list('titel', flat=True))
    if len(rezepte) > 0:
        return redirect("/zutaten/",
                        msg=f'Zutat {zutat.name} wurde nicht gelöscht. '
                            f'Es wird verwendet in "{", ".join(rezepte)}"')
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
        provider=request.provider,
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
         'preis': str(r.preis() or '--').replace('.', ','),
         'aktiv': r.aktiv}
        for r in Rezept.objects.filter(
                provider=request.provider
            ).order_by('slug')]
    data = {'planungen': planungen_js,
            'rezepte': rezepte,
            'month': month,
            'year': year,
            'gangfolge': request.provider.gaenge,
            'days_in_month': days_in_month(year, month),
            'is_authenticated': request.user.is_authenticated}
    gaenge = request.provider.gaenge.split()
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
        provider=request.provider,
    ).select_related('rezept')

    def sortkey(planung):
        return request.provider.gaenge.find(planung.gang)

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
