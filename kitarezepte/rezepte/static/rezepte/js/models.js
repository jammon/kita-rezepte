var models = (function($, _, Backbone) {
"use strict";

// This module contains
// - all the constructors for the data models (`Person`, `Ward` etc.),
// - the data models themselves (`persons`, `wards` etc.),
// - some data determining the working status 
//   (like `user_can_change`, `today_id`, `errors` etc.)

var _user_can_change = false;
function user_can_change(can_change) {
    if (arguments.length===0) return _user_can_change;
    _user_can_change = can_change;
}

// A Menu has a 
//     - Datum
//     - Koch
//     - Vorspeise
//     - Hauptgang
//     - Nachtisch
var Menu = Backbone.Model.extend({
    initialize: function() {
        var datum = this.get('datum');
        this.set('datum', new Date(datum[0], datum[1], datum[2]));
    },
});

var Menus = Backbone.Collection.extend({
    model: Menu,
    comparator: function(menu) {
        return menu.get('date');
    },
});
var menus = new Menus();

var Rezept = Backbone.Model.extend({
    initialize: function() {
        var js = this.get('js');
        
    },
});

function initialize(rezepte) {
    // body...
}

return {
    menus: menus,
    initialize: initialize,
};
})($, _, Backbone);
