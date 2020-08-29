# Kita-Rezepte

Problem mit django-tinymce als Issue gemeldet: https://github.com/aljosa/django-tinymce/issues/265

## Migration: Preis als Decimal, Menge als int
- Schritt 1:
  + Zutat.preis (Decimal) einführen
  + Rezept._preis_dec (Decimal, default=None) einführen
  + RezeptZutat.menge_int einführen
- Schritt 2:
  + Zutat.preis berechnen: Zutat.preis_pro_einheit / Decimal('100')
  + RezeptZutat.menge_int berechnen: int(RezeptZutat.menge)
- Schritt 3:
  + Zutat.preis_pro_einheit löschen
  + Rezept._preis löschen
  + RezeptZutat.menge löschen
- Schritt 4:
  + Rezept._preis_dec umbenennen in Rezept._preis
  + (RezeptZutat.menge_int umbenennen in RezeptZutat.menge)

## Test auf Zutat-Preise
Soll testen, ob die Preise nach der Migration noch gleich sind.

    with open("zutatenpreise.txt", "w") as outfile:
        for z in Zutat.objects.all().order_by('id'):
            outfile.write(f"{z.id};{z.name};{z.preisInEuro()}\n")

    with open("zutatenpreise-neu.txt", "w") as outfile:
        for z in Zutat.objects.all().order_by('id'):
            outfile.write(f"{z.id};{z.name};{z.preis}\n")

    with open("zutatenpreise-neu.txt", "r") as neu:
      with open("zutatenpreise.txt", "r") as alt:
        for a, n in zip(alt, neu):
          if n[-4]=='.':
            n = n[:-4] + ',' + n[-3:]
          if n != a:
            print(f"alt: {a}")
            print(f"neu: {n}\n")

## Häufigste Zutaten extrahieren
    import csv
    from django.db.models import Count
    from rezepte.models import Zutat
    with open('zutaten.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        for z in Zutat.objects.annotate(Count('rezepte')).order_by('-rezepte__count'):
          csvwriter.writerow([z.name, z.einheit, z.menge_pro_einheit, z.masseinheit, z.kategorie])

Die 194 häufigsten Zutaten sind in `/kitarezepte/zutaten.csv`.

## Zutaten in neuen Client importieren
Aktion im Admin.

## Allergene
Lebensmittelinformationsverordnung, in Anhang 2 ist die Liste der Allergene.
https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:02011R1169-20180101
