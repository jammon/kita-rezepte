// jshint esversion: 6
var models = (function($, _, Backbone) {
"use strict";

// collections of Rezepte for every kategorie or gang
var kategorien = {};
var gangkategorien = {};
var data = {};  // data like 'gangfolge', 'days_in_month', 'year', 'month', 'is_authenticated'


// Planung has a
// - day (1-31)
// - datum (a Date)
// - rezept
// - gang (a String like "Vorspeise")
var Planung = Backbone.Model.extend({
    initialize: function() {
        const datum = this.get('datum');
        this.set('day', datum[2]);
        this.set('datum', (new Date(datum[0], datum[1]-1, datum[2])));
        const rezept_id = this.get('rezept_id');
        if (rezept_id) {
            this.set('rezept', rezepte.get(rezept_id));
        }
    },
});


// Rezept has
// - id
// - titel
// - kategorien (Array, could be "Vorspeise" etc. or "Reisgericht" etc.) 
// - preis (in Cent)
var Rezept = Backbone.Model.extend({
    initialize: function() {
        if (!this.has('aktiv'))
            this.set('aktiv', true);
        if (this.get('aktiv')) {
            // für jede Kategorie eine eigene Collection
            this.get('kategorien').forEach(function(kategorie) {
                if (!kategorien[kategorie]) {
                    kategorien[kategorie] = new Rezepte();
                }
                kategorien[kategorie].add(this);
            }, this);
            this.get('gang').forEach(function(gang) {
                if (!gangkategorien[gang]) {
                    gangkategorien[gang] = new Rezepte();
                }
                gangkategorien[gang].add(this);
            }, this);
        }
    },
    titel_mit_preis: function() {
        if (this.get('id')==-1)
            return 'nicht geplant';
        return this.get('titel') + '  ' + this.get('preis') + ' €';
    },
});

var Zutat = Backbone.Model.extend({
    get_einheit: function() {
        if (this.get('menge_pro_einheit'))
            return this.get('masseinheit');
        return this.get('einheit');
    },
});

function is_quantitativ(value) {
    return /^\d+$/.test(value);
}
// RezeptZutat has
// - zutat - a Zutat
// - menge - an Integer *or* a string
// - nummer - an Int
var RezeptZutat = Backbone.Model.extend({
    initialize: function() {
        if (!this.get('zutat')) {
            this.set('zutat', zutaten.get({id: this.get('zutat_id')}));
        }
        let mq = this.get('menge_qualitativ');
        if (mq)
            this.set('menge', mq);
    },
    toString: function() {
        let zutat = this.get('zutat');
        let name = zutat.get('name');
        let menge = this.get('menge');
        if (is_quantitativ(menge)) {
            let einheit = zutat.get_einheit();
            if (einheit)
                return menge + ' ' + einheit + ' ' + name;
        }
        return menge + ' ' + name;
    },
    toJson: function() {
        let res = {
            zutat_id: this.get('zutat').get('id'),
            nummer: this.get('nummer'),
        };
        let menge = this.get('menge');
        if (is_quantitativ(menge))
            res.menge = parseInt(menge);
        else
            res.menge_qualitativ = menge;
        return JSON.stringify(res);
    },
    is_quantitativ: function() {
        return is_quantitativ(this.get('menge'));
    },
});

var Planungen = Backbone.Collection.extend({model: Planung});
var Rezepte = Backbone.Collection.extend({model: Rezept});
var Zutaten = Backbone.Collection.extend({model: Zutat, comparator: 'name'});
var RezeptZutaten = Backbone.Collection.extend({model: RezeptZutat, comparator: 'nummer'});
var planungen = new Planungen();
var rezepte = new Rezepte();
var zutaten = new Zutaten();
var rezeptzutaten = new RezeptZutaten();


// function preis_in_euro(preis) {
//     if (preis == '--') 
//         return preis;
//     if (preis>99) {
//         preis = preis + '';
//         return preis.slice(0, -2) + ',' + preis.slice(-2) + ' €';
//     }
//     preis = (preis + 100) + '';
//     return '0,' + preis.slice(-2) + ' €';
// }


return {
    planungen: planungen,
    rezepte: rezepte,
    zutaten: zutaten,
    rezeptzutaten: rezeptzutaten,
    Rezept: Rezept,
    Zutat: Zutat,
    RezeptZutat: RezeptZutat,
    kategorien: kategorien,
    gangkategorien: gangkategorien,
    is_quantitativ: is_quantitativ,
    data: data,
};
})($, _, Backbone);
