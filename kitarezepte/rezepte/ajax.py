# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

import json

from .models import Client, Rezept, GangPlan
from .utils import day_fromJson, get_client

@login_required
@require_POST
def set_gangplan(request):
    client_slug = get_client(request)
    if client_slug != request.session['client_slug']:
        return HttpResponse(status=403, reason="Falscher Client.")
    client = Client.objects.get(slug=client_slug)
    data = json.loads(request.body)
    try:
        rezept_id = data['rezept_id']
        datum = day_fromJson(data['datum'])
        gang = data['gang']
    except KeyError:
        return HttpResponse(status=422, reason="Fehlerhafte Anfrage.")
    try:
        rezept = Rezept.objects.get(id=rezept_id, client__slug=client_slug)
    except Rezept.DoesNotExist:
        return HttpResponse(
            status=404, reason="Rezept nicht gefunden. Rezept Id: " + str(rezept_id))
    gangplan, created = GangPlan.objects.update_or_create(
        client=client,
        datum=datum,
        gang=gang,
        defaults={'rezept': rezept})
    return JsonResponse({
        'success': 'Planung erstellt' if created else 'Planung aktualisiert',
        'rezept': {'id': rezept.id, 'titel':rezept.titel},
        'datum': str(datum),
        'gang': gang,
        })