# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

import json

from .views import get_client_query_args
from .models import Client, Rezept, GangPlan
from .utils import day_fromJson

@login_required
@require_POST
@permission_required('rezepte.add_gangplan')
def set_gangplan(request):
    data = json.loads(request.body)
    client_slug = request.session['client_slug']
    try:
        rezept_id = data['rezept_id']
        datum = day_fromJson(data['datum'])
        gang = data['gang']
    except KeyError:
        return JsonResponse({
            'error': "Fehlerhafte Anfrage.",
        })
    try:
        rezept = Rezept.objects.get(id=rezept_id, client__slug=client_slug)
    except Rezept.DoesNotExist:
        return JsonResponse({
            'error': "Rezept nicht gefunden. Rezept Id: " + str(rezept_id),
        })
    gangplan, created = GangPlan.objects.update_or_create(
        client__slug=client_slug,
        datum=datum,
        gang=gang,
        defaults={'rezept': rezept})
    return JsonResponse({
        'success': 'Planung erstellt' if created else 'Planung aktualisiert',
        'rezept': {'id': rezept.id, 'titel':rezept.titel},
        'datum': str(datum),
        'gang': gang,
        })