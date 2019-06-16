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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from rezepte import views, ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('rezepte/', views.rezepte),
    path('rezepte/<int:id>', views.rezepte),
    path('rezepte/<int:id>/edit/', views.rezepte, {'edit': True}),
    path('rezepte/<slug:slug>', views.rezepte),
    path('rezepte/<slug:slug>/edit/', views.rezepte, {'edit': True}),
    path('zutaten/', views.zutaten, name="zutaten"),
    path('zutaten/<int:id>', views.zutaten),
    path('zutaten/delete', views.zutaten_delete),
    path('monat/<int:year>/<int:month>', views.monat),
    path('monat', views.monat),
    path('einkaufsliste', views.einkaufsliste),
    path('ajax/set-gang/', ajax.set_gangplan),
    path('tests', TemplateView.as_view(template_name="rezepte/tests.html"),
         name='tests'),
    re_path(r'^tinymce/', include('tinymce.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
