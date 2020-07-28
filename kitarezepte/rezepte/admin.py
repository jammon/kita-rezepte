# -*- coding: utf-8 -*-
import csv
import os

from django.conf import settings
from django.contrib import admin, messages

from .models import (Zutat, Rezept, RezeptZutat, GangPlan, Client, Provider,
                     Domain, Editor)


class ZutatAdmin(admin.ModelAdmin):
    list_display = ('name', 'kategorie')
    list_filter = ('kategorie', 'client__name')


class RezeptZutatInline(admin.TabularInline):
    model = RezeptZutat


class KategorieListFilter(admin.SimpleListFilter):
    title = 'Kategorien'
    parameter_name = 'kategorien'

    def lookups(self, request, model_admin):
        kategorien = request.session.get('kategorien', [])
        if kategorien:
            return ((k, k) for k in kategorien)
        return super().lookups(request, model_admin)

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(kategorien__contains=value)
        return queryset


class GangListFilter(admin.SimpleListFilter):
    title = 'Gänge'
    parameter_name = 'gaenge'

    def lookups(self, request, model_admin):
        return ((g, g) for g in request.session.get('gaenge', []))

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(gang__contains=value)
        return queryset


class RezeptAdmin(admin.ModelAdmin):
    exclude = ('_preis',)
    inlines = [RezeptZutatInline, ]
    list_display = ('titel', 'kategorien')
    # TODO: das funktioniert in production nicht
    # list_filter = (GangListFilter, KategorieListFilter)
    list_filter = ('provider', 'gang', 'kategorien')
    ordering = ('slug',)


class GangPlanAdmin(admin.ModelAdmin):
    ordering = ('datum',)
    list_filter = ('gang', 'provider__name')
    date_hierarchy = 'datum'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('rezept')


class ClientAdmin(admin.ModelAdmin):
    actions = ['import_zutaten']

    def import_zutaten(self, request, queryset):
        with open(os.path.join(settings.BASE_DIR, 'zutaten.csv'),
                  'r') as csvfile:
            zutatenreader = csv.reader(csvfile, delimiter=';')
            zutaten_list = list(zutatenreader)

        zutaten = []
        for client in queryset:
            if Zutat.objects.filter(client=client).count() > 0:
                self.message_user(
                    request,
                    f"Client '{client.name}' hat schon Zutaten eingegeben",
                    messages.ERROR)
                return
            for (name, einheit, menge_pro_einheit, masseinheit,
                 kategorie) in zutaten_list:
                zutaten.append(Zutat(
                    name=name,
                    client=client,
                    einheit=einheit,
                    menge_pro_einheit=menge_pro_einheit,
                    masseinheit=masseinheit,
                    kategorie=kategorie))
        Zutat.objects.bulk_create(zutaten)
        self.message_user(
            request, "Zutaten wurden importiert", messages.SUCCESS)
    import_zutaten.short_description = \
        "Standardzutaten für neuen Client importieren"


admin.site.register(Zutat, ZutatAdmin)
admin.site.register(Rezept, RezeptAdmin)
admin.site.register(RezeptZutat)
admin.site.register(GangPlan, GangPlanAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Provider)
admin.site.register(Domain)
admin.site.register(Editor)
