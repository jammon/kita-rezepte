main.setupCsrfProtection();
$(".zutat-preis input").change(function() {
    var input = $(this);
    $.ajax({
        type: "POST",
        url: "preis/" + input.attr("zutat_id"),
        data: {preis: input.val()},
        success: function(data) {
            input.val(data.preis);
            input.attr("origvalue", data.preis);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            input.val(input.attr("origvalue"));
            input.select();
        },
        dataType: "json",
    });
});
