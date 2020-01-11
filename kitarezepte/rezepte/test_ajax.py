# -*- coding: utf-8 -*-
import json
from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from rezepte.models import Client, Editor, Rezept, GangPlan
from rezepte.utils import TEST_REZEPT


class Set_GangplanTestcase(TestCase):

    def setUp(self):
        user = User.objects.create_user('test', 'test@test.tld', 'test')
        self.rez_client = Client.objects.create(name='Test-Kita')
        Editor.objects.create(user=user, client=self.rez_client)
        self.client.force_login(user)
        session = self.client.session
        session['client_slug'] = self.rez_client.slug
        session.save()
        self.rezept = Rezept.objects.create(
            titel="Testrezept", client=self.rez_client, **TEST_REZEPT)

    def test_post(self):
        response = self.client.post(
            '/ajax/set-gang/',
            {'rezept_id': str(self.rezept.id),
             'datum': '2019-04-23',
             'gang': 'Vorspeise'},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['success'], 'Planung erstellt')
        self.assertEqual(
            data['rezept'], {'id': self.rezept.id, 'titel': self.rezept.titel})

        gang = GangPlan.objects.get(
            client=self.rez_client,
            datum=date(2019, 4, 23),
            gang="Vorspeise")
        self.assertEqual(gang.rezept_id, self.rezept.id)

    def test_post_wrong_client(self):
        session = self.client.session
        session['client_slug'] = 'otherclient'
        session.save()
        response = self.client.post(
            '/ajax/set-gang/',
            {'rezept_id': str(self.rezept.id),
             'datum': '2019-04-23',
             'gang': 'Vorspeise'},
            content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_post_wrong_data(self):
        # no rezept_id
        response = self.client.post(
            '/ajax/set-gang/',
            {'datum': '2019-04-23',
             'gang': 'Vorspeise'},
            content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_post_rezept_not_found(self):
        response = self.client.post(
            '/ajax/set-gang/',
            {'rezept_id': 2342,
             'datum': '2019-04-23',
             'gang': 'Vorspeise'},
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
