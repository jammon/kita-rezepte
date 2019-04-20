var views = (function($, _, Backbone) {
"use strict";

var PlanungView = Backbone.View.extend({
    // zeigt einen Gang an einem Tag
    events: {
        'click': 'edit_gang',
    },
    tagName: 'td',
    initialize: function(options) {
        this.className = this.model.get('gang');
        this.id = this.model.get('gang') + this.model.get('day');
    },
    render: function() {
        const rezept = this.model.get('rezept');
        if (rezept) {
            this.$el.text(rezept.get('titel'));
        } else {
            this.$el.text('nicht geplant');
        }
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
                    let data = {
                        day: i,
                        datum: [models.data.year, models.data.month, i],
                        gang: g,
                    };
                    planung = models.planungen.add(data);
                }
                var pv = new PlanungView({model: planung});
                row.append(pv.render().$el);
            });
            this.$el.append(row);
        }
    },
});

var dispatcher = _.clone(Backbone.Events)

return {
    PlanungView: PlanungView,
    MonatView: MonatView,
    dispatcher: dispatcher,
};
})($, _, Backbone);
