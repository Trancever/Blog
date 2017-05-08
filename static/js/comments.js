$(document).ready(function () {
    $(".comment-reply-btn").click(function (event) {
        var link = $(this);
        event.preventDefault();
        console.log("reply link clicked")
        $(this).closest(".comment").children(".comment_reply").fadeToggle("medium", function () {
            if ($(this).is(":visible")) {
                link.text("Schowaj");
            } else {
                link.text("Pokaż");
            }
        });
    })

    // Edit comment
    $(".comment-edit-btn").click(function (event) {
        event.preventDefault();
        var commentDiv = $(this).closest(".comment-not-edited");
        var editDiv = commentDiv.next(".comment-edited");
        commentDiv.toggle("medium");
        editDiv.toggle("medium");
        var content = commentDiv.find(".panel-body").text();
        var input = editDiv.find("#id_content");
        input.val(content);
        input.focus();
    })

    $("form.comment-edit").on('submit', function (event) {
        event.preventDefault();
        var comment_content = $(this).find("#id_content").val();
        if (comment_content == "") {
            console.log("Content is empty. Validation error.")
            $(this).children("#comment-content-validation-message").show();
            $(this).find("#id_content").focus();
            return;
        }
        console.log("Editing comment with ajax request");
        var comment_id = $(this).children("[name='comment_id']").val();
        edit_comment(comment_id, comment_content)
        $(this).toggle("medium");
        $(this).parent().prev(".comment-not-edited").toggle("medium");
    })

    function edit_comment(comment_id, content) {
        $.ajax({
            url: "/comments/edit_comment/", // the endpoint
            type: "POST", // http method
            data: {
                comment_id: comment_id,
                comment_content: content,
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                console.log(json.is_success)
                if (json.is_success == true) {
                    console.log("id = " + json.comment_id + ", new content = " + json.comment_content);
                    $("div#" + json.comment_id).find("#content" + json.comment_id).text(json.comment_content)
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

    $(".comment-delete").on('submit', function (event) {
        event.preventDefault();
        console.log("Deleting comment with ajax request.");
        var comment_id = $(this).children("[name='comment_id']").val()
        console.log($(this).children("[name='comment_id']"))
        delete_comment(comment_id);
    })

    function delete_comment(comment_id) {
        $.ajax({
            url: "/comments/delete_comment/", // the endpoint
            type: "POST", // http method
            data: {
                comment_id: comment_id,
            }, // data sent with the post request

            // handle a successful response
            success: function (json) {
                console.log(json.parent_id)
                console.log(json.is_success)
                if (json.is_success == true) {
                    console.log($("#" + json.parent_id))
                    $("#" + json.parent_id).hide();
                }
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };

    // Validate if user is authenticated and can post comments
    $(".comment-create").on('submit', function (event) {
        // event.preventDefault();
        console.log($("#comment-user-validator").val() )
        if ($("#comment-user-validator").val() == "False") {
            $(this).children("#comment-content-validation-message").show();
            event.preventDefault();
        }
    })
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