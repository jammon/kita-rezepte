var models = (function($, _, Backbone) {
"use strict";

var kategorien = {};
var gangkategorien = {};
var data = {};

// var _user_can_change = false;
// function user_can_change(can_change) {
//     if (arguments.length===0) return _user_can_change;
//     _user_can_change = can_change;
// }

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
var Rezept = Backbone.Model.extend({
    initialize: function() {
        // für jede Kategorie eine eigene Collection
        this.get('kategorien').forEach(function(kategorie) {
            var kategorie_obj = kategorien;
            if (data.gangfolge.indexOf(kategorie)>-1)
                kategorie_obj = gangkategorien;
            if (!kategorie_obj[kategorie]) {
                kategorie_obj[kategorie] = new Rezepte();
            }
            kategorie_obj[kategorie].add(this);
        }, this);
    },
});

var Planungen = Backbone.Collection.extend({model: Planung});
var Rezepte = Backbone.Collection.extend({model: Rezept});
var planungen = new Planungen();
var rezepte = new Rezepte();


return {
    planungen: planungen,
    rezepte: rezepte,
    kategorien: kategorien,
    gangkategorien: gangkategorien,
    data: data,
};
})($, _, Backbone);
