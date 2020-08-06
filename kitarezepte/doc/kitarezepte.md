# Kita-Rezepte
An internet application to manage recipes, cooking schedules and grocery lists for a day care center.

Eine Internetapplikation, um Rezepte, Kochpläne und Einkaufslisten für eine Kita zu verwalten.

- Alle Rezepte sind Public Domain. Sie dürfen frei verwendet werden. Jeder, der ein Rezept einstellt, muss gewährleisten, dass es frei von Rechten anderer ist und erteilt eine bedingungslose Nutzungslizenz für andere Nutzer.

## Visuelle Tests:
* Hauptseite aufrufen
* Zutatenliste anzeigen
    * Einen Preis ändern
    * eine Zutat bearbeiten
* Rezeptliste aufrufen
    * ein Rezept anzeigen
    * ein Rezept bearbeiten
        * eine Zutat löschen
        * eine Zutat hinzufügen
        * Text/Kategorie/Gang ändern
    * Rezeptliste mit Preisen anzeigen
    * Alle Rezepte (zum Ausdrucken) anzeigen
* Monatsplan aufrufen
    * ein Rezept ändern
    * einen Koch ändern
* Einkaufsliste aufrufen 


## Detail-Beschreibung
### Rezepteingabe
Zutaten:
- Man kann durch Eingabe die Auswahl der Zutaten einengen.
- Jeweils die erste Zutat ist ausgewählt.
- Mit Up/Down kann man andere Zutaten auswählen.
- Wenn man das Eingabefeld verlässt, wird die ausgewählte Zutat und ihre Einheit übernommen.
- Wenn die Eingabe keiner bekannten Zutat entspricht, dann öffnet sich ein Dialog zur Eingabe der Zutat. Diese wird nach Erfolg ins Eingabefeld und mit ihrer Einheit übernommen. 

## Clients
- Jeder Client hat eine eigene Subdomain (`<client-slug>.kita-rezepte.de` oder `<client-slug>.kitarez.uber.space`).
- Die Subdomain muss im SSL-Zertifikat berücksichtigt sein.
- Der Verweis muss auf die Hauptseite (von Hand).

### Einen neuen Client anlegen
- Die Subdomain beim Domainhoster anlegen (kann dauern). 
- Die Subdomain im Webserver anlegen. 
    + `uberspace web domain add <slug>.kita-rezepte.de`
    + `uberspace web domain add <slug>.kitarez.uber.space`
- Den Client, den Provider und die Domain in der Admin-Site anlegen.
- Editor anlegen.
- (Admin anlegen.)
- template anlegen (`rezepte/templates/rezepte/providers/<slug>.html`)
- Standardzutaten können über die Admin-Seite importiert werden

### Einrichtungen
- Ein Client kann mehrere Einrichtungen haben. 
- Jede Einrichtung hat eigene Rezepte, aber alle Zutaten sind bei einem Client gleich.
- Die Einkaufsliste gibt es nur ein Mal.
- Wenn sich ein Editor für mehrere Einrichtungen einloggt, dann bekommt er eine Auswahlseite mit den Einrichtungen.
- Ein Editor für mehrere Einrichtungen hat im Menu Links zu den anderen Einrichtungen.

## Rezepte übernehmen
- Wenn man für einen Client eingeloggt ist, kann man Rezepte eines anderen Clients übernehmen.
- Dafür hat das Rezept einen Button "Für &lt;eigene Einrichtung&gt; übernehmen".
- Die Funktion kopiert das Rezept.
- Zutaten werden übernommen
    + Wenn Zutaten beim eigenen Client nicht vorhanden sind, werden sie ohne Preis angelegt und die Mengen übernommen.
    + Wenn Zutaten vorhanden sind, und die Einheit gleich ist, werden die Mengen übernommen.
    + TODO: Wenn Zutaten vorhanden sind, und die Einheit verschieden ist, wird die Menge qualitativ übernommen. (Problem markieren?)
    + Gang und Kategorien werden nur übernommen, wenn sie beim Client vorhanden sind.

## Zutaten übernehmen
Neu eingerichtete Kitas bekommen ein Set von häufigen Zutaten ohne Preis. Das sind die Zutaten, die in der Pusteblume am häufigsten benutzt werden.

## Konfigurations-Dateien
`kitarezepte/kita-rezepte.cnf` hat etwa dieses Format:

    [django]
    key = <SECRET_KEY>

    [server]
    mode = production | development

    [mail]
    password = <EMAIL_HOST_PASSWORD>

## Designentscheidungen
### Redis
Wird nicht eingerichtet, weil die Site nicht zeitkritisch ist.

### django-pipeline etc.
Wird nicht eingerichtet, weil die Site nicht zeitkritisch ist.

### Browser
Es werden nur moderne ES6-kompatible Browser unterstützt.
