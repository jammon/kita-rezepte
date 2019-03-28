# -*- coding: utf-8 -*-
import glob
from collections import defaultdict
from os import path
from bs4 import BeautifulSoup

# In den Rezepten sind die Anmerkungen nicht drin
# Die werden anschließend aus den Menueplänen gezogen

rezepte = defaultdict(dict)
for filename in glob.glob("rezepte/*.html"):
    print("Processing ", filename)
    with open(filename) as fp:
        soup = BeautifulSoup(fp, "lxml")

    rezept = {}
    rezept['slug'] = path.splitext(path.basename(filename))[0]
    rezept['titel'] = soup.find(id='titel').string
    rezept['fuer_erwachsene'] = int(soup.find(id='erwachsene').string)
    rezept['fuer_kinder'] = int(soup.find(id='kinder').string)
    rezept['zubereitung'] = soup.find(id='zubereitung').string
    rezept['anmerkungen'] = soup.find(id='anmerkungen').string

    zutaten = {}

