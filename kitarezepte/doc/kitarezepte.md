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
- Den Client in der Admin-Site anlegen.
- Editor anlegen.
- Admin anlegen.
- Die Subdomain im Webserver anlegen. 
    + `uberspace web domain add <slug>.kita-rezepte.de`
    + `uberspace web domain add <slug>.kitarez.uber.space`
- Die Subdomain beim Domainhoster anlegen. 
- Verweis auf der Hauptseite eintragen.

## Konfigurations-Dateien

