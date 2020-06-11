var input_span = $(".zutat-preis-input");
var input_input = $(".zutat-preis-input input");
main.setupCsrfProtection();
$(".zutat-preis").click(function() {
    var display_span = $(this);
    display_span.addClass("hidden");
    var value = display_span.text();
    input_span.insertAfter(display_span);
    input_span.removeClass("hidden");
    input_input.val(value).select();
});
input_span.change(function() {
    var display_span = input_span.prev();
    $.ajax({
        type: "POST",
        url: "preis/" + display_span.attr("zutat_id"),
        data: {preis: input_input.val()},
        success: function(data) {
            input_span.addClass("hidden")
            var ds = input_span.prev();
            ds.text(data.preis);
            ds.removeClass("hidden");
        },
        error: function(jqXHR, textStatus, errorThrown) {
            input_input.select();
        },
        dataType: "json",
    });
});
