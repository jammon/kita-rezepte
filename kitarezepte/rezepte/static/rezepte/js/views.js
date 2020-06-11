// jshint esversion: 6
var views = (function($, _, Backbone) {
"use strict";

// Monat ---------------------------------------------------------
//
var planung_template;
var planung_auth_template;
function init_monat_templates() {
    if ($('#gang-cell').length>0) 
        planung_template = _.template($('#gang-cell').html());
        planung_auth_template = _.template($('#gang-cell-auth').html());
}

var PlanungView = Backbone.View.extend({
    // zeigt einen Gang an einem Tag
    events: {
        'click': 'edit_gang',
    },
    className: 'col',
    initialize: function(options) {
        this.gangbreite = options.gangbreite;
        this.id = this.model.get('gang') + this.model.get('day');
        this.listenTo(this.model, "change", this.render);
    },
    render: function() {
        const rezept = this.model.get('rezept');
        let content;
        if (rezept.id == -1) 
            content = rezept.get('titel');
        else if (models.data.is_authenticated)
            content = planung_auth_template({rezept: rezept});
        else content = planung_template({rezept: rezept});
        this.$el.empty().append(content).addClass(
            this.model.get('gang') + ' col-md-' + this.gangbreite);
        return this;
    },
    edit_gang: function() {
        if (models.data.is_authenticated)
            dispatcher.trigger('edit_gang', this.model);
    },
});

const Tagnamen = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];
var TagView = Backbone.View.extend({
    className: 'row tag-row',
    initialize: function(options) {
        this.day = options.day;
        this.template = this.template || _.template($('#day-table').html());
    },
    render: function() {
        let day = this.day.getDate();
        let gangbreite = Math.floor(12 / models.data.gangfolge.length);
        this.$el.append(this.template({
            dayname: Tagnamen[this.day.getDay()],
            day: day,
            month: models.data.month,
            year: models.data.year,
        }));
        if ([0, 6].indexOf(this.day.getDay())==-1){
            let gaenge = this.$(".gaenge");
            models.data.gangfolge.forEach(function(g) {
                let planung = 
                    models.planungen.findWhere({day: day, gang:g}) ||
                    models.planungen.add({
                        day: day, 
                        gang: g,
                        datum: [models.data.year, models.data.month, day],
                        rezept: models.rezepte.get(-1),
                    });
                let pv = new PlanungView({model: planung, gangbreite: gangbreite});
                gaenge.append(pv.render().$el);
            });
        }
        return this;
    },
});
var MonatView = Backbone.View.extend({
    render: function() {
        for (let i = 1; i <= models.data.days_in_month; i++) {
            let dayview = new TagView({
                day: new Date(models.data.year, models.data.month-1, i)
            });
            this.$el.append(dayview.render().el);
        }
        return this;
    },
});

// Rezept - Edit ----------------------------------------------------
//
// RezeptZutatView: Zeigt eine RezeptZutat an
// ZutatenListeView: Zeigt die Liste der Rezeptzutaten
// ZutatenEingabeView: Autocomplete-Input für die Auswahl der Zutat
// NeueZutatView: Modaler Dialog für die Eingabe einer neuen Zutat
// MengenEingabeView: Input für Menge (quant. oder qual.)
// EinheitView: stellt die passende Einheiit dar
// ZutatenView: Stellt die anderen Views für die Eingabe der Zutaten dar

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
        let that = this;
        let el = this.$el;
        el.autocomplete({
            source: function(request, response) {
                let names = models.zutaten.pluck('name');
                let term = $.ui.autocomplete.escapeRegex(request.term);
                let matcher1 = new RegExp("^" + term, "i");
                let matcher2 = new RegExp("^.+" + term, "i");
                function subarray(matcher) {
                    return _.filter(names, function(item) {
                        return matcher.test(item);
                    });
                }
                response(subarray(matcher1).concat(subarray(matcher2)));
            },
            autoFocus: true,
            change: function(event, ui) { that.check_zutat(ui.item, true); },
        });
        this.listenTo(models.zutaten, "update", function(zutaten) {
            el.autocomplete("option", "source", zutaten.pluck('name'));
        });
        let neuezutatview = new NeueZutatView({el: $("#zutatModal")});
        this.listenTo(neuezutatview, "NeueZutat", this.check_zutat);
    },
    check_zutat: function(item, edited) {
        if (item) {
            this.zutat = models.zutaten.findWhere({'name': item.value});
        } else {
            let lower_name = this.$el.val().toLocaleLowerCase('de-DE');
            this.zutat = models.zutaten.find(function(zutat) {
                return zutat.get('name').toLocaleLowerCase('de-DE').indexOf(lower_name) > -1;
            });
        }
        if (this.zutat) {
            if (edited) this.$el.val(this.zutat.get('name'));
            this.trigger("zutat-selected", this.zutat);
        } else if (edited) {
            $('#add-zutat')[0].reset();
            $('#zutatModal #id_name').val(this.$el.val());
            $('#zutatModal').modal();
        }
    },
    empty: function(focus) {
        this.$el.val('');
        this.zutat = void 0;
        if (focus) this.$el.focus();
    },
});

var NeueZutatView = Backbone.View.extend({
    initialize: function() {
        let that = this;
        let zutatform = this.$('#add-zutat');
        let el = this.$el;
        zutatform.submit(function () {
            $.ajax({
                type: zutatform.attr('method'),
                url: zutatform.attr('action'),
                data: zutatform.serialize(),
                success: function (data) {
                    models.zutaten.add(JSON.parse(data.zutat));
                    el.modal('hide');
                    that.trigger("NeueZutat");
                    $("#mengeneingabe").focus();
                },
                dataType: "json",
                error: function(data) {
                    that.$(".error").html(data.responseText.slice(0, 100));
                }
            });
            return false;
        });
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
            return {menge: this.$el.val()};
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
        rz_dict.zutat = this.zutateneingabe.zutat;
        this.zutateneingabe.empty(true);
        rz_dict.nummer = models.rezeptzutaten.length;
        models.rezeptzutaten.add(rz_dict);
    },
    write_rz_inputs: function() {
        this.zutatenliste.zutaten_views.forEach(function(view, index) {
            let nr = view.$el.index();
            view.model.set('nummer', nr);
            this.$el.append($("<input>").attr({
                name: "rz" + nr,
                type: "hidden",
            }).val(view.model.toJson()));
        }, this);
    },
});

var dispatcher = _.clone(Backbone.Events);

return {
    PlanungView: PlanungView,
    MonatView: MonatView,
    init_monat_templates: init_monat_templates,
    RezeptZutatView: RezeptZutatView,
    ZutatenEingabeView: ZutatenEingabeView,
    MengenEingabeView: MengenEingabeView,
    NeueZutatView: NeueZutatView,
    ZutatenListeView: ZutatenListeView,
    ZutatenView: ZutatenView,
    dispatcher: dispatcher,
};
})($, _, Backbone);
