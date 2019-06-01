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
        this.$el.text(models.data.is_authenticated ? 
            rezept.titel_mit_preis() : 
            rezept.get('titel'));
        return this;
    },
    edit_gang: function() {
        if (models.data.is_authenticated)
            dispatcher.trigger('edit_gang', this.model);
    },
});

const Tagnamen = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"]
var MonatView = Backbone.View.extend({
    id: 'monat-table',
    render: function() {
        for (let i = 1; i <= models.data.days_in_month; i++) {
            let day = new Date(models.data.year, models.data.month-1, i);
            let row = $("<tr>", {"class": 'day-row'});
            row.append($("<td>").text(
                Tagnamen[day.getDay()] + '. ' + i + '.' + models.data.month + '.'));
            models.data.gangfolge.forEach(function(g) {
                let planung = models.planungen.findWhere({day: i, gang:g});
                if (!planung) {
                    planung = models.planungen.add({
                        day: i,
                        datum: [models.data.year, models.data.month, i],
                        gang: g,
                        rezept: models.rezepte.get(-1),
                    });
                }
                let pv = new PlanungView({model: planung});
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
    className: "list-group-item",
    events: {
        'click .delete': 'delete',
    },
    render: function() {
        this.$el.html(
            '<span class="delete">&times;</span>' + this.model.toString());
        return this;
    },
    delete: function() {
        this.$el.remove();
        this.trigger('delete', this);
    },
});

var ZutatenListeView = Backbone.View.extend({
    initialize: function() {
        var that = this;
        this.$el.sortable();
        this.listenTo(this.collection, "add", this.appendModelView);
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
        this.listenTo(view, 'delete', this.delete_model);
    },
    delete_model: function(view) {
        this.collection.remove(view.model);
        this.zutaten_views = this.zutaten_views.filter(function(v) {
            return view != v;
        });
    },
});

var ZutatenEingabeView = Backbone.View.extend({
    initialize: function() {
        var that = this;
        this.$el.autocomplete({
            source: models.zutaten.pluck('name'),
            change: function(event, ui) {
                that.check_zutat(ui.item.value, true);
            },
        });
    },
    check_zutat: function(value, edited) {
        let name = value || this.$el.val();
        this.zutat = models.zutaten.findWhere({'name': name});
        if (this.zutat) {
            this.trigger("zutat-selected", this.zutat);
        } else if (edited) {
            alert("Neue Zutat: " + name);
        }
    },
    empty: function(focus) {
        this.$el.val('');
        this.zutat = void 0;
        if (focus) this.$el.focus();
    },
});

var MengenEingabeView = Backbone.View.extend({
    events: {
        'input': 'input_changed',
        'keyup': 'maybe_enter',
    },
    initialize: function() {
        this.regex = /^\d+(,\d*)?$/;
        this.quantitativ = false;
    },
    input_changed: function(event) {
        this.quantitativ = this.regex.test(event.target.value);
        this.trigger('menge-changed', this.quantitativ);
    },
    maybe_enter: function(event) {
        if (event.key=='Enter') {
            this.trigger('menge-ready');
        }
    },
    get_menge: function() {
        if (this.quantitativ) {
            return {menge: parseFloat(this.$el.val().replace(',', '.'))};
        } else {
            return {menge_qualitativ: this.$el.val()};
        }
    },
    empty: function() {
        this.$el.val('');
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
        this.zutatenliste = (new ZutatenListeView({
            el: this.$("#zutatenliste"),
            collection: models.rezeptzutaten,
        })).render();
        this.zutateneingabe = new ZutatenEingabeView({el: this.$("#zutateneingabe")});
        this.mengeneingabe = new MengenEingabeView({el: this.$("#mengeneingabe")});
        this.einheitview = new EinheitView({el: this.$("#einheit_fuer_eingabe")});
        this.einheitview.listenTo(
            this.zutateneingabe, "zutat-selected", this.einheitview.new_unit);
        this.einheitview.listenTo(
            this.mengeneingabe, 'menge-changed', this.einheitview.change_greyed_out);
        this.listenTo(this.mengeneingabe, 'menge-ready', this.neue_zutat);
        this.zutateneingabe.check_zutat();
    },
    zutat_changed: function(zutat) {
        this.$("#einheit_fuer_eingabe").text(zutat.get_einheit());
    },
    neue_zutat: function() {
        let rz_dict = this.mengeneingabe.get_menge();
        this.mengeneingabe.empty();
        rz_dict['zutat'] = this.zutateneingabe.zutat;
        this.zutateneingabe.empty(true);
        rz_dict['nummer'] = models.rezeptzutaten.length;
        models.rezeptzutaten.add(rz_dict);
    },
    write_rz_inputs: function() {
        this.zutatenliste.zutaten_views.forEach(function(view, index) {
            this.$el.append($("<input>").attr({
                name: "rz" + view.$el.index(),
                type: "hidden",
            }).val(view.model.toJson()));
        }, this);
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
