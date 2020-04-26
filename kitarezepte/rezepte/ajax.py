# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

import json

from .forms import ZutatForm
from .models import Client, Rezept, Zutat, GangPlan
from .utils import day_fromJson, client_param


@login_required
@require_POST
@client_param
def set_gangplan(request, client_slug=''):
    if client_slug != request.session.get('client_slug'):
        return HttpResponse(status=403, reason="Falscher Client.")
    client = Client.objects.get(slug=client_slug)
    data = json.loads(request.body)
    try:
        rezept_id = data['rezept_id']
        datum = day_fromJson(data['datum'])
        gang = data['gang']
    except KeyError:
        return HttpResponse(status=422, reason="Fehlerhafte Anfrage.")
    if rezept_id == '-1':
        count, _ = GangPlan.objects.filter(
            client=client, datum=datum, gang=gang
        ).delete()
        return JsonResponse({
            'success': 'Planung ' + ('gelöscht' if count else 'nicht gefunden'),
            'rezept': {'id': -1, 'titel': 'nicht geplant'},
            'datum': str(datum),
            'gang': gang,
        })

    try:
        rezept = Rezept.objects.get(id=rezept_id, client__slug=client_slug)
    except Rezept.DoesNotExist:
        return HttpResponse(
            status=404,
            reason="Rezept nicht gefunden. Rezept Id: " + str(rezept_id))
    gangplan, created = GangPlan.objects.update_or_create(
        client=client,
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
@client_param
def add_zutat(request, client_slug=''):
    if client_slug != request.session.get('client_slug'):
        return HttpResponse("Falscher Client.", status=403)
    client = get_object_or_404(Client, slug=client_slug)
    form = ZutatForm(request.POST, instance=Zutat(client=client))
    if form.is_valid():
        if form.cleaned_data['name'] == 'ERROR':
            return HttpResponse("Error requested.", status=400)
        zutat = form.save()
        resp = JsonResponse({
            'success': 'xxx',
            'zutat': zutat.toJson()})
        return resp
    return HttpResponse('Form is not valid', status=400)
