# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Zutat, Rezept, RezeptZutat, GangPlan, Client, Editor


class ZutatAdmin(admin.ModelAdmin):
    list_display = ('name', 'kategorie')
    list_filter = ('kategorie', )


class RezeptZutatInline(admin.TabularInline):
    model = RezeptZutat

class KategorieListFilter(admin.SimpleListFilter):
    title ='Kategorien'
    parameter_name = 'kategorien'

    def lookups(self, request, model_admin):
        return ((k, k) for k in request.session.get('kategorien', []))

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(kategorien__contains=value)
        return queryset

class GangListFilter(admin.SimpleListFilter):
    title ='Gänge'
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
    list_filter = (GangListFilter, KategorieListFilter)
    ordering = ('slug',)


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
