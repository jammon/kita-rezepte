# Usecases

- alle Models müssen Bezug auf den Mandanten nehmen √
- Mandant:
    + Stammdaten: Name etc. √
    + Essen (Frühstück, Mittagessen etc.) und Gänge (Vorspeise, Hauptgang und Nachtisch) √
- Zutaten eingeben
    + die Zutaten müssen eine Kategorie haben √
    + die Zutaten sollen einen Preis pro Menge haben √
    + Zutaten eingeben √
    + Zutaten löschen, wenn sie nicht mehr benutzt werden √
- Preis der Zutaten aktualisieren 
    + automatisch Preise der Rezepte aktualisieren √
    + Preise für viele Zutaten aktualisieren 
        * für alle Zutaten oder nur für das, was nächste Woche gebraucht wird.
- Rezepte eingeben
    + die Rezepte müssen Kategorien haben √
    + der Titel soll die URL bestimmen (als Slug) √
    + Untertitel/Anmerkung, um ähnliche Rezepte zu unterscheiden √
    + die Rezepte enthalten Zutaten mit Mengen √
    + Zutaten auswählen mit Mengenangaben √
    + Markieren nach Essen und Gang √
    + Preis errechnen √
    + abweichende Versionen von Rezepten erstellen
- Menüs für einen Tag eingeben/ändern. √
    + Feier- und Schließungstage
- Alle Menüs eines Zeitraums (Monat) anzeigen. √
    + Je nach Anmeldestatus auch Anzeige von Kosten und Bearbeitungsmöglichkeit √
- Aus den geplanten Menüs eine Einkaufsliste erstellen. √
    + Auflistung der Zutaten getrennt nach quantitativen und qualitativen Angaben √
    + Auflistung der geplanten Rezepte √
    + Zeiträume für die Einkaufsliste angeben

## Mechanismen
### Clients
- Jeder Client hat eine Domain ("fooclient.kita-rezepte.de"). √
- Der Client wird durch seinen Slug identifiziert ("fooclient"). √
- Angemeldete Nutzer gehören zu einem Client. √
- Der Client, für den der Nutzer angemeldet ist, ist in der Session. √
- Auch angemeldete Nutzer können die Rezepte etc. eines anderen Clients betrachten. Dann unterscheidet sich der Client in der Session von dem Client der Domain. √
    + In einer späteren Ausbaustufe könnten sie für unterschiedliche Clients berechtigt sein, sind aber immer für einen Client angemeldet. Dieser ist in der Session.

## Weitere Pläne
- Für jedes Rezept anzeigen, wann es die letzten Male geplant wurde (nur für angemeldete Nutzer)
- Häufig oder selten geplante Rezepte
