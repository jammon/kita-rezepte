# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from .models import Rezept, Client, Editor
from .utils import TEST_REIS, TEST_REZEPT


def create_user(name, client, email='test@test.tld', password='test'):
    user = User.objects.create_user(name, email, password)
    Editor.objects.create(user=user, client=client)
    return user


class LoginTestcase(TestCase):
    """Test login view"""

    def test_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/login.html')

    def setup_user(self):
        client = Client.objects.create(name='Test-Kita')
        create_user('test', client)

    def test_post(self):
        self.setup_user()
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             'https://test-kita.kita-rezepte.de/monat',
                             fetch_redirect_response=False)
        self.assertEqual(self.client.session['user_name'], 'test')
        self.assertEqual(self.client.session['client_slug'], 'test-kita')

    def test_post_wrong_data(self):
        self.setup_user()
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'wrong'})
        self.assertEqual(response.context['form'].is_valid(), False)

    def test_no_editor(self):
        user = User.objects.create_user('test', 'test@test.tld', 'test')
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(self.client.session['user_name'], 'test')


class WrongClientTestcase(TestCase):
    """Try to edit wrong client"""

    def setUp(self):
        self.right_client = Client.objects.create(name='Test-Kita')
        self.wrong_client = Client.objects.create(name='Wrong')
        self.right_user = create_user('Test-Kita User', self.right_client)
        self.wrong_user = create_user('Wrong User', self.wrong_client)
        Editor.objects.create(user=self.right_user, client=self.right_client)
        Editor.objects.create(user=self.wrong_user, client=self.wrong_client)


class RezepteTestcase(TestCase):
    """Test rezepte view"""

    def setUp(self):
        client = Client.objects.create(name='Test-Kita')
        self.rezept1 = Rezept.objects.create(
            titel="Testrezept1", client=client, **TEST_REZEPT)
        self.rezept2 = Rezept.objects.create(
            titel="Testrezept2", client=client, **TEST_REZEPT)

    def test_ein_rezept_id(self):
        response = self.client.get('/rezepte/' + str(self.rezept1.id))
        self.assertTemplateUsed(response, 'rezepte/rezept.html')
        self.assertEqual(response.context['recipe'], self.rezept1)

    def test_ein_rezept_slug(self):
        response = self.client.get('/rezepte/' + str(self.rezept1.slug))
        self.assertTemplateUsed(response, 'rezepte/rezept.html')
        self.assertEqual(response.context['recipe'], self.rezept1)

    def test_alle_rezepte(self):
        response = self.client.get('/rezepte/')
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        recipes = response.context['recipes']
        self.assertEqual(
            [gang for gang, rezepte in recipes],
            ["Vorspeise", "Hauptgang", "Nachtisch", "unsortiert"])
        self.assertIn(self.rezept1, recipes[1][1])
        self.assertIn(self.rezept2, recipes[1][1])

    def test_wrong_rezept_id(self):
        response = self.client.get('/rezepte/1000')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'),
                         'Rezept "1000" nicht gefunden')

    def test_wrong_rezept_slug(self):
        response = self.client.get('/rezepte/not-there')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'),
                         'Rezept "not-there" nicht gefunden')

    def test_other_clients_rezept_id(self):
        client = Client.objects.create(name='Other-Client')
        rezept = Rezept.objects.create(
            titel="Not my Testrezept", client=client, fuer_kinder=20,
            fuer_erwachsene=5, zubereitung='', anmerkungen='', kategorien='')
        response = self.client.get('/rezepte/' + str(rezept.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'), 
                         f'Rezept "{rezept.id}" nicht gefunden')
