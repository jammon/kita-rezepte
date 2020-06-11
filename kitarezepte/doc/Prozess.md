# Kita-Rezepte

## Redis als Cache-Backend
https://lab.uberspace.de/guide_redis.html
https://jazzband.github.io/django-redis/latest/

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