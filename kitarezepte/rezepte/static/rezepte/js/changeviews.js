var changeviews = (function($, _, Backbone) {
"use strict";

const allerezepte_string = "Alle Rezepte";

var ChangePlanungView = Backbone.View.extend({
    // Hat 
    // - Inputbox für Tastatureingabe
    // - Selectbox für Rezepte
    // - Selectbox für Kategorien
    // Wenn in der Inputbox Buchstaben eingegeben werden, 
    //     wird damit die Rezeptbox gefiltert.
    // Wenn in der Kategoriebox ausgewählt wird, 
    //     wird die Rezeptbox gefiltert.
    // Mit Cursortasten Auf und Ab kann in der Rezeptbox ausgewählt werden.
    // Bei "Enter" oder "Speichern" wird das gewählte Rezept gespeichert
    tagName: 'td',
    events: {
        'input #cpv-kategorien': 'filter_rezepte',
        'input #cpv-rezept': 'filter_rezepte',
        'click .submit': 'submit',
    },
    initialize: function(options) {
        views.dispatcher.on('edit_gang', this.edit_gang, this);
    },
    titel_template: _.template(
        "Planung für <%= gang %> am <%=day%>.<%=month%>.<%=year%>"),
    render: function() {
        const datum = this.planung.get('datum');
        this.$("#gangModalLabel").text(this.titel_template({
            gang: this.gang_kategorie,
            day: datum.getDate(),
            month: datum.getMonth()+1,
            year: datum.getFullYear(),
        }));
        // Inputbox
        this.$("#cpv-rezept").val('').focus();
        // Rezeptbox
        this.$("#cpv-rezepte").html(
            this.rezepte.map(function(rezept) {
                return $("<option>").val(rezept.id).text(rezept.get("titel"));
            })
        );
        // Kategoriebox
        var kategorien = Object.keys(models.kategorien).sort();
        kategorien.unshift(allerezepte_string);
        this.$("#cpv-kategorien").html(_.map(kategorien, function(kategorie) {
            return $("<option>").val(kategorie).text(kategorie)
                                .addClass('kategorie-option');
        }));
        return this;
    },
    filter_rezepte: function(kategorie_changed) {
        let kat_string = this.$("#cpv-kategorien").val();
        let kategorie = void 0;
        if (kat_string && kat_string!=allerezepte_string)
            kategorie = models.kategorien[kat_string];
        let input = this.$("#cpv-rezept").val();
        let regex = new RegExp('.*' + input + '.*', 'i');
        let options = this.$("#cpv-rezepte").children();
        options.map(function() {
            $(this).toggleClass(
                "hidden", 
                !((!kategorie || kategorie.get(this.value)) &&
                  regex.test(this.text)));
        });
        if (options.is(":selected.hidden")) {
            let visible = options.filter(function() {
                return !$(this).hasClass("hidden");
            });
            if (visible.length)
                visible[0].selected = true;
        }
    },
    submit: function() {
        let rezept_id = this.$("#cpv-rezepte").val();
        if (rezept_id===null || rezept_id===undefined)
            return;
        alert(models.rezepte.get(rezept_id).get('titel') + "gewählt");
    },
    edit_gang: function(planung) {
        this.planung = planung;
        this.gang_kategorie = this.planung.get('gang');
        this.rezepte = models.gangkategorien[this.gang_kategorie];
        this.render().$el.modal();
    },
});
var changeplanungview = new ChangePlanungView({el: $("#gangModal")});

return {
    ChangePlanungView: ChangePlanungView,
};
})($, _, Backbone);
