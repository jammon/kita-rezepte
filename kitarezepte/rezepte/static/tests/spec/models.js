describe("Rezept", function() {
    it("should initialize kategorien", function() {
        models.data.gangfolge = ['Vorspeise', 'Hauptgang', 'Nachtisch'];
        let r = new models.Rezept({
            name: 'Spaghetti',
            gang: ['Hauptgang',],
            kategorien: ['Nudelgericht',],
        });
        expect(models.gangkategorien.Hauptgang.length).toBe(1);
        expect(models.gangkategorien.Hauptgang.at(0).get('name')).toBe('Spaghetti');
        expect(models.kategorien.Nudelgericht.length).toBe(1);
        expect(models.kategorien.Nudelgericht.at(0).get('name')).toBe('Spaghetti');
    });
});
describe("RezeptZutat", function() {
    it("should form a proper String", function() {
        let reis = new models.Zutat({
            name: "Reis", 
            einheit: "1 kg",
            preis_pro_einheit: 189,
            menge_pro_einheit: 1000,
            masseinheit: "g",
            kategorie: "Grund."
        });
        let rz = new models.RezeptZutat({
            zutat: reis,
            menge: 500,
        });
        expect(rz.toString()).toBe("500 g Reis");

        rz = new models.RezeptZutat({
            zutat: reis,
            menge_qualitativ: "etwas",
        });
        expect(rz.toString()).toBe("etwas Reis");

        let eier = new models.Zutat({
            name: "Eier",
            einheit: "",
        });
        rz = new models.RezeptZutat({
            zutat: eier,
            menge: 3,
        });
        expect(rz.toString()).toBe("3 Eier");
    });
});
describe("preis_in_euro", function() {
    it("should represent ints as amount of Euros", function(){
        expect(models.preis_in_euro('--')).toEqual('--');
        expect(models.preis_in_euro(0)).toEqual('0,00 €');
        expect(models.preis_in_euro(1)).toEqual('0,01 €');
        expect(models.preis_in_euro(90)).toEqual('0,90 €');
        expect(models.preis_in_euro(99)).toEqual('0,99 €');
        expect(models.preis_in_euro(100)).toEqual('1,00 €');
        expect(models.preis_in_euro(589)).toEqual('5,89 €');
    });
});
