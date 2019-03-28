# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Zutat, Rezept, RezeptZutat, Menue, Gang, Client


class KategorienMixin(object):

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('kategorie')

    def kategorien(self, obj):
        return u", ".join(o.name for o in obj.kategorie.all())

class ZutatAdmin(admin.ModelAdmin):
    list_display = ('name', 'kategorie')
    list_filter = ('kategorie', )


class RezeptZutatInline(admin.TabularInline):
    model = RezeptZutat


class RezeptAdmin(admin.ModelAdmin, KategorienMixin):
    inlines = [RezeptZutatInline, ]
    list_display = ('titel', 'kategorien')
    list_filter = ('kategorie', )


admin.site.register(Zutat, ZutatAdmin)
admin.site.register(Rezept, RezeptAdmin)
admin.site.register(RezeptZutat)
admin.site.register(Menue)
admin.site.register(Gang)
admin.site.register(Client)
