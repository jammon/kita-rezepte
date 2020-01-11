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

## Log des Einlesens
Zutat "7 St. TK Spinat" konnte bei Rezept-Id 511 nicht gelesen werden
Zutat "2 Pckg. Schafskäse" konnte bei Rezept-Id 556 nicht gelesen werden
Zutat "3400 g Kartoffeln" konnte bei Rezept-Id 562 nicht gelesen werden
Zutat "1000 g Kartoffeln" konnte bei Rezept-Id 595 nicht gelesen werden
Zutat "2000 g Sauerkraut" konnte bei Rezept-Id 639 nicht gelesen werden
Zutat "150 g Walnussbruch" konnte bei Rezept-Id 649 nicht gelesen werden
Zutat "200 g Walnüsse" konnte bei Rezept-Id 661 nicht gelesen werden
Zutat "200 g Walnussbruch" konnte bei Rezept-Id 677 nicht gelesen werden
Zutat "300 g Walnussbruch" konnte bei Rezept-Id 678 nicht gelesen werden
Zutat "1 Pckg. Schafskäse" konnte bei Rezept-Id 679 nicht gelesen werden
Zutat "200 g gehackte Mandeln" konnte bei Rezept-Id 706 nicht gelesen werden
lies https://kita-rezepte.appspot.com/monatsplan/2019/8
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2019/7
lies https://kita-rezepte.appspot.com/monatsplan/2019/6
lies https://kita-rezepte.appspot.com/monatsplan/2019/5
lies https://kita-rezepte.appspot.com/monatsplan/2019/4
Rezept nicht gefunden "Erbsencremesuppe"
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
lies https://kita-rezepte.appspot.com/monatsplan/2019/3
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2019/2
lies https://kita-rezepte.appspot.com/monatsplan/2019/1
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
lies https://kita-rezepte.appspot.com/monatsplan/2018/12
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2018/11
lies https://kita-rezepte.appspot.com/monatsplan/2018/10
Rezept nicht gefunden "Erbsencremesuppe"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2018/9
lies https://kita-rezepte.appspot.com/monatsplan/2018/8
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2018/7
lies https://kita-rezepte.appspot.com/monatsplan/2018/6
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2018/5
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2018/4
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
lies https://kita-rezepte.appspot.com/monatsplan/2018/3
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2018/2
lies https://kita-rezepte.appspot.com/monatsplan/2018/1
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
lies https://kita-rezepte.appspot.com/monatsplan/2017/12
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2017/11
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2017/10
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2017/9
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2017/8
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2017/7
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2017/6
Rezept nicht gefunden "Möhrencremesuppe mit Curry"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2017/5
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2017/4
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "3K Ragout"
lies https://kita-rezepte.appspot.com/monatsplan/2017/3
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Broccoliecremesuppe mit Croutons (reduzierte Menge)"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2017/2
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
lies https://kita-rezepte.appspot.com/monatsplan/2017/1
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
lies https://kita-rezepte.appspot.com/monatsplan/2016/12
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2016/11
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Überbackene Spinatpfannkuchen"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
lies https://kita-rezepte.appspot.com/monatsplan/2016/10
Rezept nicht gefunden ""
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
lies https://kita-rezepte.appspot.com/monatsplan/2016/9
Rezept nicht gefunden "Broccoliecremesuppe mit Croutons (reduzierte Menge)"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
lies https://kita-rezepte.appspot.com/monatsplan/2016/8
Rezept nicht gefunden "Dinkelburger mit fränkischem Kartoffelsalat"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2016/7
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Hirseschnitzel mit Tomatensoße / Dipp"
Rezept nicht gefunden "Milchreis mit Obst"
lies https://kita-rezepte.appspot.com/monatsplan/2016/6
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Milchreis mit Obst"
lies https://kita-rezepte.appspot.com/monatsplan/2016/5
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2016/4
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Kartoffel-Möhrensuppe"
lies https://kita-rezepte.appspot.com/monatsplan/2016/3
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2016/2
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Winterobst (Banane, Apfel, Ananas, Orange)"
lies https://kita-rezepte.appspot.com/monatsplan/2016/1
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden "Gemüserisotto"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2015/12
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Winterobst (Kiwi, Banane, Orange, Apfel)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Möhrencremesuppe mit Curry und Ingwer"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2015/11
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "3K Ragout"
lies https://kita-rezepte.appspot.com/monatsplan/2015/10
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "3K Ragout"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Milchreis mit Obst"
lies https://kita-rezepte.appspot.com/monatsplan/2015/9
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Buntes Ofengemüse"
Rezept nicht gefunden "Milchreis mit Obst"
lies https://kita-rezepte.appspot.com/monatsplan/2015/8
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Rohkost (Paprika/Möhren/Radieschen/saure Gurken)"
Rezept nicht gefunden "Joghurt mit Nüssen und Honig"
lies https://kita-rezepte.appspot.com/monatsplan/2015/7
Rezept nicht gefunden "Milchreis mit Obst"
Rezept nicht gefunden "Erbsencremesuppe mit Vollkorntoast"
Rezept nicht gefunden "Gries-Buttermilch-Dessert m. Pfirsich"
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
Rezept nicht gefunden ""
lies https://kita-rezepte.appspot.com/monatsplan/2015/6
Einlesen erfolgreich.
260 Zutaten, 287 Rezepte, 2946 Pläne eingelesen.
Gelesen:
Zutaten: 260
Rezeptzutaten: 2156
Rezepte: 287
Anmerkungen: 26
Pläne: 2946


Rezept "Humus mit Brot" hat schon Untertitel "ganzes Jahr".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Spinat-Lasagne Luca" hat schon Untertitel "Ein Rezept von Tanja für das ganze Jahr".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Möhrenrisotto" hat schon Untertitel "Ein Rezept von Susanne Louven-Kemna".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Kürbislasagne" hat schon Untertitel "Bewährtes Kita-Rezept für ein Gericht von September bis April".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Griechischer Bauernsalat" hat schon Untertitel "Ein Rezept von Susanne Louven-Kemna".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Gewürzmöhren mit Hirse" hat schon Untertitel "Falls möglich Möhren mit Grün liefern lassen".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Buchweizenauflauf" hat schon Untertitel "Rezept für das ganze Jahr".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "gedünstete Möhren mit Mais" hat schon Untertitel "Wird nicht gerne gegessen!".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Broccolicremesuppe mit Croutons" hat schon Untertitel "Ein Rezept von Franzi Matoni".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Blattsalat" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Gnocchi-Gemüse-Pfanne" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Apfelrotkohl mit Kartoffelpüree" hat schon Untertitel "Wintergericht".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Rigatoni verdi" hat schon Untertitel "Rezept von Andrea Gutzmann".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Seemannskonfetti" hat schon Untertitel "in Anlehnung an "Kochen für Kindergruppen" Katrin Raschke".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "gelbe Linsensuppe mit Orangensaft" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Untertitel alt: None.
    Untertitel neu: ein Rezept von Sabine Hattenkerl für ein Gericht im ganzen Jahr.
Rezept "Obstsalat I." hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen!".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Möhren-Kokosmilchsuppe " hat schon Anmerkungen "Bitta eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Eintopf mit Chinakohl" hat schon Untertitel "Wintergericht".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Verstecktes Gemüse" hat schon Untertitel "Für den Winter, da mit TK-Gemüse zuzubereiten".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Griessflammerie mit Obst" hat schon Untertitel "Rezept von Susanne luven-Kemna für ein Gericht im ganzen Jahr (u.U. das Obst variieren)".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Spinat-Lasagne" hat schon Untertitel "Rezept von Tine German-Nagels".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Vanillepudding mit Birnen" hat schon Untertitel "Obst nach Saison ".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Bunter Gemüsekuchen" hat schon Untertitel "Rezept von Silke Bacht".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Tomatensuppe mit Mozarella" hat schon Untertitel "Rezept von Franzi für ein Gericht im Sommer".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Pellkartoffeln mit Kräuterquark" hat schon Untertitel "Ein Gericht für den Frühsommer".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Multiple - "gegrillte Maiskolben" existiert mehrfach.
Rezept "Kartoffel-Frittata mit Blattsalat" hat schon Untertitel "Ein Rezept für das ganze Jahr / Zur Tomatenzeit auch frische Tomaten möglich!".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "fruchtiger Milchreis mit Kruste" hat schon Untertitel "Rezept von Janine".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Polenta-Lauch-Auflauf" hat schon Untertitel "Ein Rezept von Torsten Hattenkerl für ein Gericht im ganzen Jahr".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Rezept "Thunfischbratlinge mit Möhrensalat und Dipp" hat schon Anmerkungen "Bitte für Marie-France Dinkel-Burger mit Thunfisch und geraspelten Möhren machen".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Weißkohlsalat mit Ananas" hat schon Untertitel "Die Kinder essen den Salat nicht gerne, zum großen Teil gar nicht!".
    Die Untertitel wären gleich.
    Die Anmerkungen wären gleich.
Too long - Bei "Risotto mit Tofu" ist der Untertitel zu lang: "Ein Rezept von Uschi Lepski
RISOTTOREIS WURDE DURCH EINFACHEN REIS ERSETZT, DA NACH MEINUNG DES 
"KOCHS" DER RISOTTOREIS ZU MÄCHTIG WAR. BITTE SELBST ENTSCHEIDEN!".
Rezept "Vollkornbaguette/ Vollkorntoast/Vollkornbrötchen" hat schon Anmerkungen "Das Gericht enthält folgende Allergene: glutenhaltiges Getreide".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Gemüsepaella" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Salat mit Sonnenblumenkernen" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Zucchinicremesuppe" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Untertitel alt: None.
    Untertitel neu: Rezept für den Sommer/Herbst.
Multiple - "Cous-Cous-Salat" existiert mehrfach.
Rezept "Ananas" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Gemischter Salat (Mais und Gurke)" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Blattsalat mit roter Beete" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Fruchteis" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Apfel-Möhren-Salat" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "gedünsteter Möhrensalat" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Untertitel alt: None.
    Untertitel neu: Rezept von Andrea Barck.
Rezept "Salat mit Mais" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "gemischter Salat" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Überbackene Bananen in Orangensauce" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Multiple - "Gegrillte Maiskolben" existiert mehrfach.
Rezept "Eisbergsalat mit Apfelstückchen" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Apfelmus " hat schon Anmerkungen "Bitte vom Selbstgekochtem Apfelmus eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Salat mit Gurke und Mais" hat schon Anmerkungen "Biite eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Klare Suppe mit Gemüse-/Reiseinlage" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
Rezept "Möhren-Trauben-Salat" hat schon Anmerkungen "Bitte eine Rückstellprobe anfertigen.".
    Die Anmerkungen wären gleich.
    Die Untertitel wären gleich.
59 Rezepte aktualisiert.
