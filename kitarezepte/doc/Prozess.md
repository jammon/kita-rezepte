# Kita-Rezepte

Problem mit django-tinymce als Issue gemeldet: https://github.com/aljosa/django-tinymce/issues/265

## Test auf Zutat-Preise
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
