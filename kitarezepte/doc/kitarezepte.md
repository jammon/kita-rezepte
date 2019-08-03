# Kita-Rezepte
An internet application to manage recipes, cooking schedules and grocery lists for a day care center.

Eine Internetapplikation, um Rezepte, Kochpläne und Einkaufslisten für eine Kita zu verwalten.

- Alle Rezepte sind Public Domain. Sie dürfen frei verwendet werden. Jeder, der ein Rezept einstellt, muss gewährleisten, dass es frei von Rechten anderer ist und erteilt eine bedingungslose Nutzungslizenz für andere Nutzer.

## Nutzerverwaltung
Auf [www.kita-rezepte.de/auth/users](http://www.kita-rezepte.de/auth/users) kann man Nutzer eintragen und löschen.

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

## Erweiterung 
- Man soll Rezepte von anderen Kitas übernehmen können
- Bei Eingabe neuer Zutaten evtl. die Zutaten anderer Kitas zur Auswahl anbieten.

## User Stories

Zutaten einpflegen              ok
    mit Einheit                 ok
    Menge pro Einheit           ok
Zutaten wieder löschen
  cave Referenzen, evtl. nur ersetzen, andere Packungsgröße angeben, 
    als nicht mehr verfügbar markieren
Preise für viele Zutaten aktualisieren                                   ok
    für alle Zutaten oder nur für das, was nächste Woche gebraucht wird. ok
Zeiträume festlegen (für Rezeptplan oder Einkaufsplan)
    Freieingabe                                                          ok 
    Standardzeiträume: nächste/r Woche/Monat, nächste Einkaufsperiode
        evtl. als Vorbelegung per Javascript
Rezept eingeben
    Felder/Informationen:                                       ok
        Titel
        Untertitel/Kommentar
        Auswahl von Zutaten mit Menge
        Zubereitung (Text)
        "Berechnet für" x Kinder und y Erwachsene
        Anmerkungen (Spezialzubereitung für einzelne Kinder)
        eingegeben von (User)
        geeignet als: Vorspeise, Hauptgang, Nachtisch
    Preis für Rezept anzeigen                                   ok
    Spezialdarstellung der Zutaten mit Preisen                  ok
    Versionen von Rezepten
        Mengen, Zutaten oder Zubereitung können abweichen
        sind unter dem gleichen Namen abgelegt.
Menüplan für 1 Tag zusammenstellen
    Kategorie: Suppe, Teigwaren, Gemüse, Getreide, Reis, Kartoffel, Lieblingsgerichte
    Preis des Menüplans (aufgeschlüsselt nach Gängen)
    Spezialdarstellung der Zutaten mit Preisen
Menüplan für 1 Tag ausdrucken
    mit Ankreuz-/Kommentarfeldern
Rating für den Menüplan eingeben:
    Datum, User
    kam gut an? (durchgefallen, schmeckte nicht so, war ok, gut geschmeckt, Lieblingsgericht)
    Menge ok? (viel zu wenig, knapp, richtig, reichlich, blieb viel übrig)
    wieviele Erw./Kinder haben gegessen?
    wurde die Menge angepasst?
    Geburtstagsmuffins am Vormittag? einkalkuliert?
Wochen- oder Monatsplan zusammenstellen
    Feier-/Schließungstage angeben
    für jeden Werktag:
        Koch
        Menüplan
    anfangs ist Koch noch nicht bekannt
Monatsplan ausdrucken
Einkaufsplan für einen Zeitraum machen
Text mit Detailanweisungen (z.B. bzgl. Hummus mit Brot) oder allgemeinen Festlegungen

Anmeldung einrichten
Berechtigungen vergeben

Auf einer HTML-Seite den Inhalt eines Requests ausgeben lassen     ok

Mengenangaben:                                                     ok
    Packungseinheit (für Bestellung), ggf. umzurechnen in g/ml
    in Gramm, ml oder andere Einheit wie bei der Zutat angegeben ('Tüte') - für Rezept
    oder freie Angabe ('eine Prise') - für Rezept
    
Standard-Mengenangaben (für Einkauf) in Zutateneingabe vorsehen
    z.B. 1 kg, 500 g, 1 l
    mit jQuery die Felder ausfüllen
    
