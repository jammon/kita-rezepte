# -*- coding: utf-8 -*-
import requests
import re
from django.core.management.base import BaseCommand, CommandError
from collections import defaultdict
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from datetime import date

from rezepte.models import Zutat, Rezept, RezeptZutat, GangPlan, ZUTATENKATEGORIEN

zutaten = []
zutat_dict = {}
rezepte = []
rezept_dict = {}
rezept_zutaten = []
gangplaene = []
zutatenkategorien = {lang: kurz for kurz, lang in ZUTATENKATEGORIEN}
gelesen = defaultdict(int)

def euro2cent(euro):
    """ Calculates the Cents from an Euro string. 

    Can raise ValueError
    """
    return int(round(100*float(euro.replace(',', '.'))))

mengeprog = re.compile(
    '(?P<einheit>.*\s*)(\((?P<menge_pro_einheit>.*) (?P<masseinheit>.*)\))?')

class Command(BaseCommand):
    help = 'Importiert die Inhalte von kita-rezepte.de'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int)

    def handle(self, *args, **options):
        self.client_id = options['client_id']
        self.read_zutaten()
        self.read_rezepte()
        RezeptZutat.objects.bulk_create(rezept_zutaten)
        self.read_monatsplaene()

        self.stdout.write(self.style.SUCCESS('Einlesen erfolgreich.'))
        self.stdout.write('{} Zutaten, {} Rezepte, {} Pläne eingelesen.'.format(
            len(zutaten), len(rezepte), len(gangplaene)))
        self.stdout.write('Gelesen:')
        for k, v in gelesen.items():
            self.stdout.write('{}: {}'.format(k, v))
        GangPlan.objects.bulk_create(gangplaene)

# zutaten ------------------------------------------------------------------
    def read_zutaten(self):
        r = requests.get('https://kita-rezepte.appspot.com/zutaten')
        soup = BeautifulSoup(r.text, 'html.parser')
        zutatentable = soup.find(id="col1_content").table
        for tr in zutatentable.find_all('tr')[1:]:
            zutat = self.get_zutat(tr)
            if zutat is not None:
                zutaten.append(zutat)
                zutat_dict[zutat.name] = zutat
                gelesen['Zutaten'] +=1
        Zutat.objects.bulk_create(zutaten)

    def get_zutat(self, soup):
        cols = soup.find_all('td')
        name = cols[0].string
        if not name:
            return None
        kategorie = soup.find(class_='zutatkategorie').string
        zutat = {
            'name': name,
            'preis_pro_einheit': euro2cent(soup.find(class_='zutatpreis').string),
            'kategorie': (zutatenkategorien[kategorie] 
                          if kategorie in zutatenkategorien else 'Sonst.'),
            'client_id': self.client_id,
            'id': len(zutaten) + 1,
        }
        menge = self.get_menge(cols[1].string)
        if menge:
            zutat.update({
                'einheit': menge['einheit'],
                'masseinheit': menge['masseinheit'] or '',
                'menge_pro_einheit': int(menge['menge_pro_einheit'] or 0)
            })
        return Zutat(**zutat)
        
    def get_menge(self, text):
        """ Mengenangaben extrahieren    """
        if not text:
            return None
        match = mengeprog.match(text)
        res = match.groupdict()
        res['einheit'] = res['einheit'].strip()
        return res


    # rezepte ------------------------------------------------------------------
    def read_rezepte(self):
        """ Rezepte einlesen

        rezeptbuch enthält nicht die Kategorien
        rezept/... enthält nicht die Anmerkungen (für nicht Angemeldete)

        Es gibt doppelte Rezepte mit gleichem Namen. Deshalb ist `rezepte` ein list.
        """
        r = requests.get('https://kita-rezepte.appspot.com/rezepte')
        soup = BeautifulSoup(r.text, 'html.parser')
        spalten = (soup.find(id="col2_content"), soup.find(id="col3_content"))
        with open('Rezeptbuch.html', 'r') as infile:
            self.rezeptbuch = BeautifulSoup(infile, 'html.parser')
        for spalte in spalten:
            for node in spalte.find_all('a'):
                rezept = self.read_rezept(node['href'])
                if rezept is not None:
                    rezepte.append(rezept)
                    rezept_dict[rezept.titel] = rezept
                    gelesen['Rezepte'] +=1

    def read_rezept(self, url):
        r = requests.get('https://kita-rezepte.appspot.com/' + url)
        soup = BeautifulSoup(r.text, 'html.parser')
        titel = soup.find(id='titel')
        if not (titel and titel.string):
            return None
        rezept_dict = {
            'titel': titel.string,
            'client_id': self.client_id,
            'fuer_kinder': soup.find(id='kinder').string,
            'fuer_erwachsene': soup.find(id='erwachsene').string,
            'zubereitung': ''.join(map(str, soup.find(id='zubereitung').contents)),
            'gang': soup.find(id='rezept_gang').string,
        }
        div = self.rezeptbuch.find('h4', string=rezept_dict['titel'])
        rezept_dict['anmerkungen'] = div.parent.find(class_="anmerkungen").string or ''
        if rezept_dict['anmerkungen']:
            gelesen['Anmerkungen'] +=1
        rezept = Rezept.objects.create(**rezept_dict)
        kategorie = soup.find(id='kategorie').string
        if kategorie:
            rezept.kategorie.add(kategorie)

        for nr, tr in enumerate(soup.find(id='zutatenliste').find_all('tr')):
            rz = self.read_rezeptzutat(tr.td.string, rezept.id, nr+1)
            if rz is not None:
                rezept_zutaten.append(rz)
                gelesen['Rezeptzutaten'] +=1
        return rezept

    def read_rezeptzutat(self, string, rezept_id, nummer):
        maxsplit = 0
        while True:
            tokens = string.split(maxsplit=maxsplit)
            if len(tokens) < maxsplit+1:
                self.stdout.write(
                    'Zutat "{}" konnte bei Rezept-Id {} nicht gelesen werden'.format(
                        string, rezept_id))
                return None
            name = tokens[-1]
            if name in zutat_dict:
                rz = {
                    'zutat_id': zutat_dict[name].id,
                    'rezept_id': rezept_id,
                    'nummer': nummer
                }
                if maxsplit == 2 and zutat_dict[name].masseinheit == tokens[1]:
                    rz['menge'] = float(tokens[0])
                else:
                    rz['menge_qualitativ'] = string[:-len(name)].strip()
                return RezeptZutat(**rz)
            maxsplit += 1


    # monatsplaene ------------------------------------------------------------------
    def read_monatsplaene(self):
        """ Monatspläne einlesen

        Wenn es zwei gleichnamige Rezepte gibt, werden die hier nicht differenziert.
        """
        monat = 8
        jahr = 2019
        while True:
            url = 'https://kita-rezepte.appspot.com/monatsplan/{}/{}'.format(jahr, monat)
            print('lies', url)
            r = requests.get(url)
            if r.status_code != requests.codes.ok:
                break
            soup = BeautifulSoup(r.text, 'html.parser')
            for tr in soup.find_all(class_='menue'):
                tds = tr.find_all('td')
                tag = tds[0].a.string.strip()[:-1]
                datum = date(jahr, monat, int(tag))
                self.read_gangplan(datum, 'Vorspeise', tds[2].span.string.strip())
                self.read_gangplan(datum, 'Hauptgang', tds[3].span.string.strip())
                self.read_gangplan(datum, 'Nachtisch', tds[4].span.string.strip())

            monat -= 1
            if monat == 0:
                monat = 12
                jahr -= 1

    def read_gangplan(self, datum, gang, rezept_titel):
        if rezept_titel not in rezept_dict:
            self.stdout.write('Rezept nicht gefunden "%s"' % rezept_titel)
            return
        gangplan = GangPlan(
            client_id = self.client_id,
            datum = datum,
            rezept = rezept_dict[rezept_titel],
            gang = gang)
        gangplaene.append(gangplan)
        gelesen['Pläne'] +=1
        return gangplan
