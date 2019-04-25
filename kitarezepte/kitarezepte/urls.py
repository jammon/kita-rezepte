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
from django.urls import path
from rezepte import views, ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/rezepte/$', views.rezepte),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/rezepte/(?P<id>[0-9]+)$', views.rezepte),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/rezepte/(?P<slug>[a-z0-9]+)$', views.rezepte),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/zutaten/$', views.zutaten),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/zutaten/(?P<id>[0-9]+)$', views.zutaten),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/monat/(?P<year>[0-9]+)/(?P<month>[0-9]+)$',
        views.monat),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/monat/?$', views.monat),
    url(r'(?P<client_slug>[a-z0-9_\-]+)/ajax/set-gang/?$', ajax.set_gangplan),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
