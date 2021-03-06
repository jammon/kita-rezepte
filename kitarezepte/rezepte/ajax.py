# -*- coding: utf-8 -*-
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_POST

import json

from .forms import ZutatForm
from .models import Rezept, Zutat, GangPlan
from .utils import check_provider, day_fromJson


@login_required
@require_POST
@check_provider
def set_gangplan(request):
    data = json.loads(request.body)
    try:
        rezept_id = data['rezept_id']
        datum = day_fromJson(data['datum'])
        gang = data['gang']
    except KeyError:
        return HttpResponse("Fehlerhafte Anfrage.", status=422)
    if rezept_id == '-1':
        count, _ = GangPlan.objects.filter(
            provider=request.provider, datum=datum, gang=gang
        ).delete()
        return JsonResponse({
            'success': 'Planung ' + ('gelöscht' if count else 'nicht gefunden'),
            'rezept': {'id': -1, 'titel': 'nicht geplant'},
            'datum': str(datum),
            'gang': gang,
        })

    try:
        rezept = Rezept.objects.get(
            id=rezept_id, provider=request.provider, aktiv=True)
    except Rezept.DoesNotExist:
        return HttpResponseNotFound(
            "Rezept nicht gefunden. Rezept Id: " + str(rezept_id))
    gangplan, created = GangPlan.objects.update_or_create(
        provider=request.provider,
        client=request.client,
        datum=datum,
        gang=gang,
        defaults={'rezept': rezept})
    return JsonResponse({
        'success': 'Planung erstellt' if created else 'Planung aktualisiert',
        'rezept': {'id': rezept.id, 'titel': rezept.titel},
        'datum': str(datum),
        'gang': gang,
    })


@login_required
@require_POST
@check_provider
def add_zutat(request):
    form = ZutatForm(
        request.POST, instance=Zutat(client=request.client))
    if form.is_valid():
        if form.cleaned_data['name'] == 'ERROR':
            return HttpResponse("Error requested.", status=400)
        zutat = form.save()
        resp = JsonResponse({
            'success': 'xxx',
            'zutat': zutat.toJson()})
        return resp
    return HttpResponse('Form is not valid', status=400)


@login_required
@require_POST
@check_provider
def zutat_preis(request, zutat_id=0):
    """ Den Preis einer Zutat ändern """
    try:
        zutat = Zutat.objects.get(
            id=zutat_id,
            client_id=request.session.get('client_id'))
    except Zutat.DoesNotExist:
        return HttpResponseNotFound('Zutat nicht gefunden')
    if 'preis' not in request.POST:
        return HttpResponse("Fehlerhafte Anfrage.", status=422)
    try:
        zutat.preis = Decimal(
            request.POST['preis'].replace(',', '.')
        ).quantize(Decimal('1.00'))
        zutat.preis_pro_einheit = int(zutat.preis * 100)
    except (InvalidOperation, ValueError):
        if request.POST['preis'] == '':
            zutat.preis = None
            zutat.preis_pro_einheit = -1
        else:
            return HttpResponse("Fehlerhaftes Datenformat.", status=422)
    zutat.save()
    return JsonResponse(
        {'preis': '' if zutat.preis is None
            else str(zutat.preis).replace('.', ',')})
