# -*- coding: utf-8 -*-
import glob
import re
from datetime import date
from os import path
from bs4 import BeautifulSoup, Tag

# from rezepte.models import Zutat  # , Rezept, RezeptZutat, Menue

ZUTATEN_FILE = "content/zutaten.html"
REZEPTE_FILES = "content/rezepte/*.html"
MENUEPLAN_FILES = "content/menueplan/*.html"
OUTFILE = "content/all_data.json"

zutaten = {}
rezepte = {}
menueplaene = {}


class Zutat(object):
    pass


def getZutaten():
    # name = models.CharField(max_length=25)
    # einheit = models.CharField(
    #     max_length=10, default='',
    #     help_text='''Packungseinheit für den Einkauf meist 1 kg, 1 l,
    #          aber auch 2,5 kg-Sack.
    #          Fällt weg bei Dingen wie Eiern, die eine natürliche Einheit
    #          haben; dann "Stück"''')
    # preis_pro_einheit = models.IntegerField(
    #     help_text='der Preis einer Packungseinheit; in Cent')
    # menge_pro_einheit = models.IntegerField(
    #     help_text='Anzahl der masseinheiten (s.u.) pro Packungseinheit; '
    #     'bei 1 kg: 1000')
    # masseinheit = models.CharField(max_length=5, choices=MASSEINHEITEN)
    # kategorie = models.CharField(max_length=6, choices=ZUTATENKATEGORIEN,
    #                              verbose_name='Kategorie')
    print("Sammle Zutaten")
    einheit_expr = re.compile("\s+\((\d+) (.*)\).*")
    with open(ZUTATEN_FILE) as fp:
        soup = BeautifulSoup(fp, "lxml")
        for row_nr, row in enumerate(soup.table.find_all('tr')):
            if row_nr == 0:
                continue
            zutat = Zutat()
            cells = row.find_all('td')
            zutat.name = cells[0].string
            zutat.einheit = ""
            zutat.menge_pro_einheit = 0
            zutat.masseinheit = ""
            if cells[1].string:
                einheiten = cells[1].string.splitlines()
                zutat.einheit = einheiten[0]
                if len(einheiten) > 1:
                    std_einh = einheit_expr.match(einheiten[1])
                    if std_einh:
                        zutat.menge_pro_einheit = int(std_einh.group(1) or 0)
                        zutat.masseinheit = std_einh.group(2) or ''
            ppe = row.find(class_="zutatpreis").string
            zutat.preis_pro_einheit = int(''.join(ppe.split(',')))
            zutat.kategorie = cells[3].string
            # print("Zutat:    ", zutat.name)
            # print("Einheit:  ", zutat.einheit)
            # print("Preis:    ", zutat.preis_pro_einheit / 100)
            # print("Menge:    ", zutat.menge_pro_einheit)
            # print("Mass:     ", zutat.masseinheit)
            # print("Kategorie:", zutat.kategorie)
            # print()

            if zutat.name in zutaten:
                print("Doppelte Zutat: ", zutat.name)
                break
            zutaten[zutat.name] = zutat


def getRezepte():
    # In den Rezepten sind die Anmerkungen nicht drin
    # Die werden anschließend aus den Menueplänen gezogen

    print("Sammle Rezepte")
    for filename in glob.glob(REZEPTE_FILES):
        # print("Processing ", filename)
        with open(filename) as fp:
            soup = BeautifulSoup(fp, "lxml")

        rezept = {}
        rezept['slug'] = path.splitext(path.basename(filename))[0]
        rezept['titel'] = soup.find(id='titel').string
        rezept['fuer_erwachsene'] = int(soup.find(id='erwachsene').string)
        rezept['fuer_kinder'] = int(soup.find(id='kinder').string)
        zubereitung = ''.join(
            str(t) for t in soup.find(id='zubereitung').contents)
        rezept['zubereitung'] = zubereitung
        rezept['zutaten'] = []
        r_zutaten = soup.find(id='zutatenliste').table
        for row in r_zutaten.find_all('tr'):
            zstring = row.td.string
            if zstring.startswith('  ') and zstring[2:] in zutaten:
                rezept['zutaten'].append({
                    'zutat': zutaten[zstring[2:]],
                    'menge_qualitativ': ''
                })
                continue
            for maxsplit in (2, 1, 3, 4):
                splitted = zstring.split(maxsplit=maxsplit)
                zutat = splitted[-1]
                if zutat in zutaten:
                    rz = {'zutat': zutaten[zutat]}
                    try:
                        menge = int(splitted[0])
                        menge_absolut = True
                    except ValueError:
                        menge_absolut = False
                    if menge_absolut and (maxsplit == 1 or (
                            maxsplit == 2 and
                            splitted[1] == zutaten[zutat].masseinheit)):
                        rz['menge'] = menge
                    else:
                        rz['menge_qualitativ'] = ' '.join(splitted[:-1])
                    rezept['zutaten'].append(rz)
                    break
            else:
                print("Unlesbare Zutat: {:<25} in Rezept: {}".format(
                    zstring, rezept['titel']))
        if rezept['slug'] in rezepte:
            print("Doppeltes Rezept:", rezept['slug'])
        rezepte[rezept['slug']] = rezept

    print("Sammle Menuepläne und Anmerkungen")
    GAENGE = ("Vorspeise", "Hauptgang", "Nachtisch")
    PREFIX_LEN = len("content/menueplan/")
    for filename in glob.glob(MENUEPLAN_FILES):
        with open(filename) as fp:
            soup = BeautifulSoup(fp, "lxml")
        sdatum = filename[PREFIX_LEN:PREFIX_LEN + 10]
        # datum = date(int(sdatum[:4]), int(sdatum[5:7]), int(sdatum[8:10]))
        menueplan = {'datum': sdatum}
        menueplaene[sdatum] = menueplan
        if soup.h2.string == "Menü nicht gefunden" or \
                soup.find("a", href="/rezepte/kita_geschlossen"):
            menueplan["geschlossen"] = True
            continue
        for nr, h2 in enumerate(soup.find_all('h2')):
            if nr == 0:
                assert h2.string.startswith("Es kocht")
                continue  # Koch wird wohl nicht mehr genutzt
            gang = GAENGE[nr - 1]
            assert h2.contents[0].startswith(gang)
            slug = h2.a['href'][len("/rezepte/"):]
            rezept = rezepte[slug]
            menueplan[gang.lower()] = rezept
            for s in h2.next_siblings:
                if (isinstance(s, Tag) and s["class"] == ["subcolumns"]):
                    anmerkung = soup.find(class_="anmerkungen")
                    if anmerkung:
                        rezepte[slug]['anmerkungen'] = ''.join(
                            str(t) for t in anmerkung.div.contents)
                        for id_anm in anmerkung.find_all(id="anmerkungen"):
                            id_anm.unwrap()
                    break


def write_data():
    print("Schreibe Daten")
    with open(OUTFILE) as outfile:
        pass  # TODO


if __name__ == '__main__':
    getZutaten()
    getRezepte()
    write_data()


# Kommentare:
# In "Tortellinisalat, lauwarm" ist in der Zubereitung Mozarella erwähnt,
# in der Zutatenliste aber nicht.

# In "Gurken-Melonen-Salat" steht in den Zutaten "2 St. Mozarella".
# Es gibt bei den Zutaten Mozarella à 100 g und à 200 g.
# Ich habe im Rezept 200 g Mozarella daraus gemacht
# und bei den Zutaten nur Mozarella à 100 g drin gelassen

# In "Zucchinipuffer mit Kräuterquark" steht bei den Zutaten "Kartoffeln",
# ich habe "Kartoffeln, mehlig" daraus gemacht.
# In "Kartoffel-Möhren-Gratin" steht bei den Zutaten "Kartoffeln",
# ich habe "Kartoffeln, festkochend" daraus gemacht.
# In "Nudel-Spinat-Auflauf" steht bei den Zutaten "TK Spinat",
# ich habe "TK Spinat (Blatt)" daraus gemacht.
