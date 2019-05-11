var main = (function($, _, Backbone) {
"use strict";

function setupCsrfProtection() {
    // Implement the js part of csrf protection
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}


function initialize_monat(initdata) {
    setupCsrfProtection();
    _.extend(models.data, {
        gangfolge: initdata.gangfolge.split(' '),
        days_in_month: initdata.days_in_month,
        year: initdata.year,
        month: initdata.month,
    });
    models.rezepte.reset(initdata.rezepte);
    models.rezepte.add({
        id: -1,
        titel: "nicht geplant",
        kategorien: models.data.gangfolge,
    });
    models.planungen.reset(initdata.planungen);
    // Backbone.history.start({ pushState: true });
}

function initialize_rezept_edit(initdata) {
    models.zutaten.reset(initdata.zutaten);
    models.rezeptzutaten.reset(initdata.rezeptzutaten);
    (new views.ZutatenView({el: $("#zutaten")})).render();
}

return {
    initialize_monat: initialize_monat,
    initialize_rezept_edit: initialize_rezept_edit,
};
})($, _, Backbone);
