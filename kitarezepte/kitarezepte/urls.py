"""kitarezepte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from rezepte import views, ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('impressum/',
         TemplateView.as_view(template_name="impressum.html")),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html',
            success_url="/password_change_done/")),
    path('password_change_done/', TemplateView.as_view(
        template_name="registration/password_changed.html")),
    path('rezepte/', views.rezepte),
    path('rezepte/new', views.rezept_edit),
    path('rezepte/<int:id>', views.rezepte),
    path('rezepte/<int:id>/edit/', views.rezept_edit, name="rezept_edit"),
    path('rezepte/<int:id>/takeover/', views.rezept_takeover),
    path('rezepte/<slug:slug>', views.rezepte),
    path('rezepte/<slug:slug>/edit/', views.rezept_edit),
    path('zutaten/', views.zutaten, name="zutaten"),
    path('zutaten/<int:id>', views.zutat_edit),
    path('zutaten/preis/<int:zutat_id>', ajax.zutat_preis),
    path('zutaten/delete', views.zutaten_delete),
    path('monat/<int:year>/<int:month>', views.monat),
    path('monat', views.monat),
    path('tag/<int:year>/<int:month>/<int:day>', views.tag),
    path('tag', views.tag),
    path('einkaufsliste/<int:year>/<int:month>/<int:day>/<int:dauer>',
         views.einkaufsliste),
    path('einkaufsliste', views.einkaufsliste),
    path('ajax/set-gang/', ajax.set_gangplan),
    path('ajax/add-zutat/', ajax.add_zutat),
    path('choose_provider', views.choose_provider),
    path('providers', views.providers, name="providers"),
    path('tests', TemplateView.as_view(template_name="rezepte/tests.html"),
         name='tests'),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    path('favicon.ico', RedirectView.as_view(
        url='/static/favicon.ico', permanent=True)),
    re_path(r'^tinymce/', include('tinymce.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
