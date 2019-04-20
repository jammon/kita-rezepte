# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from rezepte.models import Rezept, Client, Editor
# from rezepte.views import 


class LoginTestcase(TestCase):
    """Test login view"""

    def test_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/login.html')

    def setup_user(self):
        user = User.objects.create_user('test', 'test@test.tld', 'test')
        client = Client.objects.create(name='Test-Kita')
        Editor.objects.create(user=user, client=client)

    def test_post(self):
        self.setup_user()
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/test-kita/monat')
        self.assertEqual(self.client.session['user_name'], 'test')
        self.assertEqual(self.client.session['client_slug'], 'test-kita')

    def test_post_wrong_data(self):
        self.setup_user()
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'wrong'})
        self.assertEqual(response.context['form'].is_valid(), False)


REZEPT = dict(
            fuer_kinder = 20,
            fuer_erwachsene = 5,
            zubereitung = '',
            anmerkungen = '',
            ist_vorspeise = True,
            ist_hauptgang = False,
            ist_nachtisch = False,
            kategorie = '')


class RezepteTestcase(TestCase):
    """Test rezepte view"""

    def setUp(self):
        client = Client.objects.create(name='Test-Kita')
        self.rezept1 = Rezept.objects.create(
            titel="Testrezept1", client=client, **REZEPT)
        self.rezept2 = Rezept.objects.create(
            titel="Testrezept2", client=client, **REZEPT)

    def test_ein_rezept_id(self):
        response = self.client.get('/test-kita/rezepte/' + str(self.rezept1.id))
        self.assertTemplateUsed(response, 'rezepte/ein-rezept.html')
        self.assertEqual(response.context['recipe'], self.rezept1)

    def test_ein_rezept_slug(self):
        response = self.client.get('/test-kita/rezepte/' + str(self.rezept1.slug))
        self.assertTemplateUsed(response, 'rezepte/ein-rezept.html')
        self.assertEqual(response.context['recipe'], self.rezept1)

    def test_alle_rezepte(self):
        response = self.client.get('/test-kita/rezepte/')
        self.assertTemplateUsed(response, 'rezepte/alle-rezepte.html')
        self.assertIn(self.rezept1, response.context['recipes'])
        self.assertIn(self.rezept2, response.context['recipes'])

    def test_anderer_client(self):
        response = self.client.get('/andere-kita/rezepte/')
        self.assertEqual(response.status_code, 404)
        client = Client.objects.create(name='Andere Kita')
        response = self.client.get('/{}/rezepte/'.format(client.slug))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/alle-rezepte.html')
        self.assertEqual(len(response.context['recipes']), 0)
