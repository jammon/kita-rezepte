var views = (function($, _, Backbone) {
"use strict";

// Monat ---------------------------------------------------------
//
var PlanungView = Backbone.View.extend({
    // zeigt einen Gang an einem Tag
    events: {
        'click': 'edit_gang',
    },
    tagName: 'td',
    initialize: function(options) {
        this.className = this.model.get('gang');
        this.id = this.model.get('gang') + this.model.get('day');
        this.listenTo(this.model, "change", this.render);
    },
    render: function() {
        const rezept = this.model.get('rezept');
        this.$el.text(rezept.get('titel'));
        return this;
    },
    edit_gang: function() {
        dispatcher.trigger('edit_gang', this.model);
    },
});

var MonatView = Backbone.View.extend({
    id: 'monat-table',
    render: function() {
        for (let i = 1; i <= models.data.days_in_month; i++) {
            var row = $("<tr>", {"class": 'day-row'});
            row.append($("<td>").text(i + '.' + models.data.month + '.'));
            models.data.gangfolge.forEach(function(g) {
                var planung = models.planungen.findWhere({day: i, gang:g});
                if (!planung) {
                    planung = models.planungen.add({
                        day: i,
                        datum: [models.data.year, models.data.month, i],
                        gang: g,
                        rezept: models.rezepte.get(-1),
                    });
                }
                var pv = new PlanungView({model: planung});
                row.append(pv.render().$el);
            });
            this.$el.append(row);
        }
        return this;
    },
});

// Rezept - Edit ----------------------------------------------------
//
var RezeptZutatView = Backbone.View.extend({
    tagName: 'li',
    render: function() {
        this.$el.text(this.model.toString());
        return this;
    },
});

var ZutatenListeView = Backbone.View.extend({
    zutaten_views: [],
    initialize: function() {
        var that = this;
        this.$el.sortable({
            update: function(event, ui) {
                that.listUpdate();
            },
        });
    },
    render: function() {
        this.$el.children().remove();
        this.zutaten_views = [];
        this.collection.each(this.appendModelView, this);
        return this;
    },    
    appendModelView: function(model) {
        var view = new views.RezeptZutatView({model: model}).render();
        this.$el.append(view.el);
        this.zutaten_views.push(view);
    },
    listUpdate: function() {
        _.each(this.zutaten_views, function(view){
            view.model.set('nummer', view.$el.index());
        });
    }
});

var ZutatenEingabeView = Backbone.View.extend({

    initialize: function() {
        var that = this;
        this.$el.autocomplete({
            source: models.zutaten.pluck('name'),
            change: function(event, ui) {
                that.zutat_changed(ui.item.value);
            },
        });
    },
    zutat_changed: function(value) {
        let zutat = models.zutaten.findWhere({'name': value});
        if (zutat) {
            this.trigger("zutat-selected", zutat);
        } else {
            alert("Neue Zutat: " + value);
        }
    },
});

var MengenEingabeView = Backbone.View.extend({
    events: {
        'input': 'input_changed',
    },
    initialize: function() {
        this.regex = /^\d+(,\d*)?$/
    },
    input_changed: function(event) {
        this.trigger('menge-changed', this.regex.test(event.target.value));
    },
});

var EinheitView = Backbone.View.extend({
    new_unit: function(zutat) {
        this.$el.text(zutat.get_einheit());
    },
    change_greyed_out: function(enabled) {
        this.$el.toggleClass('text-muted', !enabled);
    },
});

var ZutatenView = Backbone.View.extend({
    initialize: function() {
        this.zutatenliste = new ZutatenListeView({
            el: this.$("#zutatenliste"),
            collection: models.rezeptzutaten,
        });
        this.zutateneingabe = new ZutatenEingabeView({el: this.$("#zutateneingabe")});
        this.mengeneingabe = new MengenEingabeView({el: this.$("#mengeneingabe")});
        this.einheitview = new EinheitView({el: this.$("#einheit_fuer_eingabe")});
        this.einheitview.listenTo(
            this.zutateneingabe, "zutat-selected", this.einheitview.new_unit)
        this.einheitview.listenTo(
            this.mengeneingabe, 'menge-changed', this.einheitview.change_greyed_out)
    },
    zutat_changed: function(zutat) {
        this.$("#einheit_fuer_eingabe").text(zutat.get_einheit());
    },
});

var dispatcher = _.clone(Backbone.Events)

return {
    PlanungView: PlanungView,
    MonatView: MonatView,
    RezeptZutatView: RezeptZutatView,
    ZutatenEingabeView: ZutatenEingabeView,
    MengenEingabeView: MengenEingabeView,
    ZutatenListeView: ZutatenListeView,
    ZutatenView: ZutatenView,
    dispatcher: dispatcher,
};
})($, _, Backbone);
