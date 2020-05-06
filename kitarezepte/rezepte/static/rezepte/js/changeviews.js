// jshint esversion: 6
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
        'dblclick #cpv-rezepte': 'submit',
        'keydown': 'keyAction'
    },
    initialize: function(options) {
        views.dispatcher.on('edit_gang', this.edit_gang, this);
        this.kat_input_template = this.kat_input_template || _.template($("#kat-input").html());
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
                let opt = $("<option>").val(rezept.id).text(rezept.get("titel"));
                if (rezept==this.current_rezept)
                    opt.attr("selected", "selected");
                return opt;
            }, this)
        );
        // Kategoriebox
        var kategorien = Object.keys(models.kategorien).sort();
        kategorien.unshift(allerezepte_string);
        let templ = this.kat_input_template;
        this.$("#cpv-kategorien").html(_.map(kategorien, function(kategorie, i) {
            return templ({kategorie: kategorie, i: i});
        }));
        this.$(".error").empty();
        return this;
    },
    filter_rezepte: function(kategorie_changed) {
        let kat_string = this.$('input[name=inp-kat]:checked').val();
        let kategorie;
        if (kat_string && kat_string!=allerezepte_string)
            kategorie = models.kategorien[kat_string];
        let input = this.$("#cpv-rezept").val();
        let regex = new RegExp('.*' + input + '.*', 'i');
        let options = this.$("#cpv-rezepte").children();
        // hide filtered options
        options.map(function() {
            $(this).toggleClass(
                "hidden", 
                !((!kategorie || kategorie.get(this.value)) &&
                  regex.test(this.text)));
        });
        // if selection is hidden, select first option
        if (options.is(":selected.hidden")) {
            let visible = options.filter(function() {
                return !$(this).hasClass("hidden");
            });
            if (visible.length)
                visible[0].selected = true;
        }
    },
    keyAction: function(e) {
        let key = e.key;
        if (key == "ArrowDown" || key == "Down") {
            this.next_rezept(true, e);
        } else if (key == "ArrowUp" || key == "Up") {
            this.next_rezept(false, e);
        }
    },
    next_rezept: function(forward, e) {
        let selected = this.$("#cpv-rezepte>option:selected");
        if (selected.length) {
            let next = selected[forward ? 'next' : 'prev']();
            if (next.length) next[0].selected = true;
        } else {
            let options = this.$("#cpv-rezepte>option");
            options[forward ? 0 : options.length-1].selected = true;
        }
        e.preventDefault();
    },
    submit: function() {
        let rezept_id = this.$("#cpv-rezepte").val();
        if (rezept_id===null || rezept_id===undefined)
            return;
        this.save_gang(rezept_id);
    },
    edit_gang: function(planung) {
        this.planung = planung;
        this.current_rezept = planung.get('rezept');
        this.gang_kategorie = planung.get('gang');
        this.rezepte = models.gangkategorien[this.gang_kategorie];
        this.render().$el.modal();
    },
    save_gang: function(rezept_id) {
        let that = this;
        function error (jqXHR, textStatus, errorThrown) {
            that.$(".error").text(errorThrown);
        }
        function success(data) {
            that.planung.set('rezept', models.rezepte.get(data.rezept.id));
            that.$el.modal('hide');
        }
        $.ajax({
            method: "POST",
            url: '/ajax/set-gang/', 
            data: JSON.stringify({
                rezept_id: rezept_id,
                datum: date_str(this.planung.get('datum')),
                gang: this.gang_kategorie,
            }),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            error: error,
            success: success,
            context: this,
        });
    },

});

function date_str(date) {
    function twodigits(nr) {
        if (nr<10) 
            return '0' + nr;
        return '' + nr;
    }
    return date.getFullYear() + '-' + twodigits(date.getMonth()+1) + 
           '-' + twodigits(date.getDate());
}
return {
    ChangePlanungView: ChangePlanungView,
};
})($, _, Backbone);
