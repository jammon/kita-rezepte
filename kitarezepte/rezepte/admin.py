# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Zutat, Rezept, RezeptZutat, GangPlan, Client, Editor


class KategorienMixin(object):

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('kategorie')

    def kategorien(self, obj):
        return ", ".join(o.name for o in obj.kategorie.all())


class ZutatAdmin(admin.ModelAdmin):
    list_display = ('name', 'kategorie')
    list_filter = ('kategorie', )


class RezeptZutatInline(admin.TabularInline):
    model = RezeptZutat


class RezeptAdmin(admin.ModelAdmin, KategorienMixin):
    exclude = ('_preis',)
    inlines = [RezeptZutatInline, ]
    list_display = ('titel', 'kategorien')
    list_filter = ('kategorie', 'gang')


class GangPlanAdmin(admin.ModelAdmin):
    ordering = ('datum',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('rezept')


admin.site.register(Zutat, ZutatAdmin)
admin.site.register(Rezept, RezeptAdmin)
admin.site.register(RezeptZutat)
admin.site.register(GangPlan, GangPlanAdmin)
admin.site.register(Client)
admin.site.register(Editor)
