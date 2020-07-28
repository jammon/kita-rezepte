# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from http import HTTPStatus
from .models import Rezept, Client, Provider, Domain, Editor, Zutat
from .utils import TEST_REZEPT
from .views import rezept_edit, zutat_edit, zutaten, zutaten_delete


def create_user(name, client, email='test@test.tld', password='test'):
    user = User.objects.create_user(name, email, password)
    Editor.objects.create(user=user, client=client)
    return user


class LoginTestcase(TestCase):
    """Test login view"""

    def test_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'rezepte/login.html')

    def setup_user(self):
        client = Client.objects.create(name='Test-Kita')
        provider = Provider.objects.create(
            name='Test-Kita', client=client)
        Domain.objects.create(domain='testserver', provider=provider)
        create_user('test', client)

    def test_post(self):
        self.setup_user()
        response = self.client.post(
            '/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
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

    # def test_no_editor(self):
    #     User.objects.create_user('test', 'test@test.tld', 'test')
    #     self.client.post('/login/', {'username': 'test', 'password': 'test'})
    #     self.assertEqual(self.client.session['user_name'], 'test')
    #     # TODO: what is expected here?


class WrongClientTestcase(TestCase):
    """Try to edit wrong client"""

    def setup_client_and_provider(self, name):
        client = Client.objects.create(name=name)
        provider = Provider.objects.create(name=name, client=client)
        return client, provider

    def setUp(self):
        self.right_client, self.right_provider = \
            self.setup_client_and_provider('Test-Kita')
        self.wrong_client, self.wrong_provider = \
            self.setup_client_and_provider('Wrong')
        self.right_user = create_user('Test-Kita User', self.right_client)
        self.wrong_user = create_user('Wrong User', self.wrong_client)
        self.factory = RequestFactory()

    def right_page_wrong_user(self, request):
        request.client = self.right_client
        request.provider = self.right_provider
        request.session = {
            'client_id': self.wrong_client.id,
            'client_slug': self.wrong_client.slug,
            'provider_id': self.wrong_provider.id,
            'provider_slug': self.wrong_provider.slug}
        request.user = self.wrong_user

    def test_rezept(self):
        rezept = Rezept.objects.create(
            titel="Reis", provider=self.right_provider, **TEST_REZEPT)
        request = self.factory.post(
            f"/rezepte/{str(rezept.id)}/edit", titel="Bohnen")
        self.right_page_wrong_user(request)
        response = rezept_edit(request, rezept.id)
        self.assertEqual(response.status_code, 403)
        rezept = Rezept.objects.get(id=rezept.id)
        self.assertEqual(rezept.titel, "Reis")

    def test_zutat(self):
        zutat = Zutat.objects.create(name="Reis", client=self.right_client)
        request = self.factory.post('/zutaten/'+str(zutat.id), name="Bohnen")
        self.right_page_wrong_user(request)
        response = zutat_edit(request, zutat.id)
        self.assertEqual(response.status_code, 403)
        zutat = Zutat.objects.get(id=zutat.id)
        self.assertEqual(zutat.name, "Reis")


# TODO: class ZutatenTestcase(TestCase):


class RezepteTestcase(TestCase):
    """Test rezepte view"""

    def setUp(self):
        client = Client.objects.create(name='Test-Kita')
        self.provider = Provider.objects.create(
            name='Test-Kita', client=client)
        self.domain = 'testserver'
        Domain.objects.create(domain=self.domain, provider=self.provider)
        self.rezept1 = Rezept.objects.create(
            titel="Testrezept1", provider=self.provider, **TEST_REZEPT)
        self.rezept2 = Rezept.objects.create(
            titel="Testrezept2", provider=self.provider, **TEST_REZEPT)

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
            ["Hauptgang"])
        # assume:
        # recipes == [('Hauptgang',
        #              [('keine Kategorie',
        #                [self.rezept1, self.rezept2])])])
        hauptgang, kategorien = recipes[0]
        self.assertEqual(hauptgang, 'Hauptgang')
        kat, rezepte = kategorien[0]
        self.assertEqual(kat, 'keine Kategorie')
        self.assertEqual(len(rezepte), 2)
        self.assertIn(self.rezept1, rezepte)
        self.assertIn(self.rezept2, rezepte)

        REZEPT = TEST_REZEPT.copy()
        REZEPT["gang"] = "Vorspeise Nachtisch"
        Rezept.objects.create(
            titel="Vorspeise Nachtisch", provider=self.provider, **REZEPT)
        recipes = self.client.get('/rezepte/').context['recipes']
        self.assertEqual(
            [gang for gang, rezepte in recipes],
            ["Vorspeise", "Hauptgang", "Nachtisch"])

    def test_wrong_rezept_id(self):
        response = self.client.get('/rezepte/1000')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'),
                         'Rezept "1000" nicht gefunden')

    def test_wrong_rezept_slug(self):
        response = self.client.get('/rezepte/not-there')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'),
                         'Rezept "not-there" nicht gefunden')

    def test_other_clients_rezept_id(self):
        client = Client.objects.create(name='Other-Client')
        provider = Provider.objects.create(
            name='Other-Provider', client=client)
        rezept = Rezept.objects.create(
            titel="Not my Testrezept", provider=provider, fuer_kinder=20,
            fuer_erwachsene=5, zubereitung='', anmerkungen='', kategorien='')
        response = self.client.get('/rezepte/' + str(rezept.id))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'rezepte/rezepte.html')
        self.assertEqual(response.context.get('msg'),
                         f'Rezept "{rezept.id}" nicht gefunden')


class RobotsTxtTests(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        lines = response.content.decode().splitlines()
        self.assertEqual(lines[0], "User-agent: *")

    def test_post_disallowed(self):
        response = self.client.post("/robots.txt")
        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)
