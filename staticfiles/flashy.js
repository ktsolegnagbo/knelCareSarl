function flashy(message, tags) {
    var data = '<div style="padding:1px 5px 1px 5px; font-size:14px;" class="alert alert-' + tags + '" role="alert">' + message + '</div>'
    // var data = '<div class="alert alert-' + tags + '" role="alert">' + message + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span> </button> </div>'

    if (tags == 'success') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "25%" }, 1100, "swing")
            .animate({ marginRight: "20%" }, 400, "swing")
            .animate({ marginRight: "0%" }, 400, "swing")
            .animate({ marginRight: "5%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 200, "swing")
            .animate({ marginRight: "2%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 200, "swing")
            .animate({ marginRight: "1%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .delay(2800).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'warning') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "25%" }, 1100, "swing")
            .animate({ marginRight: "20%" }, 400, "swing")
            .animate({ marginRight: "0%" }, 400, "swing")
            .animate({ marginRight: "5%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 200, "swing")
            .animate({ marginRight: "2%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 200, "swing")
            .animate({ marginRight: "1%" }, 200, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .delay(3500).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'info') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "25%" }, 1000, "swing")
            .animate({ marginRight: "0%" }, 200, "swing")
            .animate({ marginRight: "3%" }, 100, "swing")
            .animate({ marginRight: "1%" }, 100, "swing")
            .animate({ marginRight: "2%" }, 100, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .animate({ marginRight: "1%" }, 100, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .delay(3100).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else if (tags == 'error') {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "25%" }, 1000, "swing")
            .animate({ marginRight: "0%" }, 800, "swing")
            .animate({ marginRight: "4%" }, 100, "swing")
            .animate({ marginRight: "2%" }, 100, "swing")
            .animate({ marginRight: "3%" }, 100, "swing")
            .animate({ marginRight: "1%" }, 100, "swing")
            .animate({ marginRight: "2%" }, 100, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .animate({ marginRight: "1%" }, 100, "swing")
            .animate({ marginRight: "0%" }, 100, "swing")
            .delay(10000).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
    else {
        $("#flash-template").html(data).appendTo("body").hide().fadeIn(800)
            .animate({ marginRight: "25%" }, 1000, "swing")
            .animate({ marginRight: "23%" }, 1000, "swing")
            .animate({ marginRight: "21%" }, 1000, "swing")
            .animate({ marginRight: "19%" }, 1000, "swing")
            .animate({ marginRight: "17%" }, 1000, "swing")
            .animate({ marginRight: "15%" }, 1000, "swing")
            .animate({ marginRight: "13%" }, 1000, "swing")
            .animate({ marginRight: "11%" }, 1000, "swing")
            .animate({ marginRight: "9%" }, 1000, "swing")
            .animate({ marginRight: "7%" }, 1000, "swing")
            .animate({ marginRight: "5%" }, 1000, "swing")
            .animate({ marginRight: "0%" }, 1000, "swing")
            .delay(3500).animate({ marginRight: "-100%" }, 3000, "swing", function () { $(this).remove(); });
    }
}