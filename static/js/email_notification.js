$(document).ready(function () {

    $("form#message-form").on("submit", function (event) {
        event.preventDefault();

        let validationOK = true;
        let validationElement = 0

        let fullname = $(this).find("#id_fullname").val();
        if (fullname.length < 3) {
            validationElement = $("#fullname-empty-error");
            validationElement.show();
            validationElement.prev(".controls").addClass("error");
            validationOK = false;
        } else {
            validationElement = $("#fullname-empty-error");
            validationElement.hide();
            validationElement.prev(".controls").removeClass("error");
        }

        let email = $(this).find("#id_email").val();
        if (validateEmail(email) === false) {
            validationElement = $("#email-wrong-format-error");
            validationElement.show();
            validationElement.prev(".controls").addClass("error");
            validationOK = false;
        } else {
            validationElement = $("#email-wrong-format-error");
            validationElement.hide();
            validationElement.prev(".controls").removeClass("error");
        }

        let message = $(this).find("#id_message").val();
        if (message.length < 20) {
            validationElement = $("#message-empty-error");
            validationElement.show();
            validationElement.prev(".controls").addClass("error");
            validationOK = false;
        } else {
            validationElement = $("#message-empty-error");
            validationElement.hide();
            validationElement.prev(".controls").removeClass("error");
        }

        if (validationOK === false) {
            return;
        }

        send_message_via_ajax(fullname, email, message);
    });

    function validateEmail(email) {
        var re = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        return re.test(email)
    }


    function send_message_via_ajax(fullname, email, message) {
        $.ajax({
            url: "/contact/send/", // the endpoint
            type: "POST", // HTTP method
            data: {
                fullname: fullname,
                email: email,
                message: message,
            },

            // handle a successful response
            success: function (json) {
                if (json.is_success == true) {
                    console.log("Email has been sent.");
                    $("div.notification").show();
                    $("div.form").hide();
                }
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }

    // Validating email form
    function addErrors() {
        $("#div_id_fullname").append("<p class='validation-message' style='display: none;' id='fullname-empty-error'>To pole musi zawierać przynajmniej 3 znaki.</p>");
        $("#div_id_email").append("<p class='validation-message' style='display: none;' id='email-wrong-format-error'>Wprowadź adres e-mail o poprawnym formacie.</p>");
        $("#div_id_message").append("<p class='validation-message' style='display: none;' id='message-empty-error'>To pole musi zawierać przynajmniej 20 znaków.</p>");
    }

    addErrors();

});

$(document).on({
    ajaxStart: function () {
        console.log($(".modal-loading"))
        $(".modal-loading").css("display", "block");
        console.log("start")
    },
    ajaxComplete: function () {
        $(".modal-loading").css("display", "none");
        console.log("stop")
    }
})


$(function () {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
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

    /*
     The functions below will create a header with csrftoken
     */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});