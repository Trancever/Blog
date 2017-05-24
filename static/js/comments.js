$(document).ready(function () {

    function setEvents() {
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
        });

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
        });

        $(".comment-delete").on('submit', function (event) {
            event.preventDefault();
            console.log("Deleting comment with ajax request.");
            var comment_id = $(this).children("[name='comment_id']").val()
            console.log($(this).children("[name='comment_id']"))
            delete_comment(comment_id);
        });

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
        });

        // Validate if user is authenticated and can post comments
        $(".comment-create").on('submit', function (event) {
            event.preventDefault();
            console.log($("#comment-user-validator").val())
            if ($("#comment-user-validator").val() == "False") {
                $(this).children("#comment-content-validation-message").show();
                return;
            }

            let object_id = $(this).find("#id_object_id").val();
            let content_type = $(this).find("#id_content_type").val();
            let comment_content = $(this).find("textarea#id_content").val();
            let parent_id = $(this).find("[name='parent_id']").val();
            let csrf_token = $(this).find("[name='csrfmiddlewaretoken']").val();
            console.log(object_id)
            console.log(content_type)
            console.log(comment_content)
            console.log(parent_id)
            console.log(csrf_token)
            create_comment(object_id, content_type, comment_content, parent_id, csrf_token);
        });
    }

    function offEvents() {
        $(".comment-reply-btn").off();
        $(".comment-edit-btn").off();
        $(".comment-delete").off();
        $("form.comment-edit").off();
        $(".comment-create").off();
    }

    setEvents();

    // $(".comment-reply-btn").click(function (event) {
    //     var link = $(this);
    //     event.preventDefault();
    //     console.log("reply link clicked")
    //     $(this).closest(".comment").children(".comment_reply").fadeToggle("medium", function () {
    //         if ($(this).is(":visible")) {
    //             link.text("Schowaj");
    //         } else {
    //             link.text("Pokaż");
    //         }
    //     });
    // })
    //
    // // Edit comment
    // $(".comment-edit-btn").click(function (event) {
    //     event.preventDefault();
    //     var commentDiv = $(this).closest(".comment-not-edited");
    //     var editDiv = commentDiv.next(".comment-edited");
    //     commentDiv.toggle("medium");
    //     editDiv.toggle("medium");
    //     var content = commentDiv.find(".panel-body").text();
    //     var input = editDiv.find("#id_content");
    //     input.val(content);
    //     input.focus();
    // })

    // $("form.comment-edit").on('submit', function (event) {
    //     event.preventDefault();
    //     var comment_content = $(this).find("#id_content").val();
    //     if (comment_content == "") {
    //         console.log("Content is empty. Validation error.")
    //         $(this).children("#comment-content-validation-message").show();
    //         $(this).find("#id_content").focus();
    //         return;
    //     }
    //     console.log("Editing comment with ajax request");
    //     var comment_id = $(this).children("[name='comment_id']").val();
    //     edit_comment(comment_id, comment_content)
    //     $(this).toggle("medium");
    //     $(this).parent().prev(".comment-not-edited").toggle("medium");
    // })

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

    // $(".comment-delete").on('submit', function (event) {
    //     event.preventDefault();
    //     console.log("Deleting comment with ajax request.");
    //     var comment_id = $(this).children("[name='comment_id']").val()
    //     console.log($(this).children("[name='comment_id']"))
    //     delete_comment(comment_id);
    // })

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

    // // Validate if user is authenticated and can post comments
    // $(".comment-create").on('submit', function (event) {
    //     event.preventDefault();
    //     console.log($("#comment-user-validator").val())
    //     if ($("#comment-user-validator").val() == "False") {
    //         $(this).children("#comment-content-validation-message").show();
    //         return;
    //     }
    //
    //     let object_id = $(this).find("#id_object_id").val();
    //     let content_type = $(this).find("#id_content_type").val();
    //     let comment_content = $(this).find("textarea#id_content").val();
    //     let parent_id = $(this).find("[name='parent_id']").val();
    //     let csrf_token = $(this).find("[name='csrfmiddlewaretoken']").val();
    //     console.log(object_id)
    //     console.log(content_type)
    //     console.log(comment_content)
    //     console.log(parent_id)
    //     console.log(csrf_token)
    //     create_comment(object_id, content_type, comment_content, parent_id, csrf_token);
    // })

    function create_comment(object_id, content_type, comment_content, parent_id, csrf_token) {
        $.ajax({
            url: "/comments/create_comment/",
            type: "POST",
            data: {
                object_id: object_id,
                content_type: content_type,
                comment_content: comment_content,
                parent_id: parent_id,
            },

            success: function (json) {
                if (json.success == false) {
                    return;
                }
                if (parent_id === undefined) {
                    let comment_div = $("#comments");
                    comment_div.prepend(get_parent_comment_html(json.comment_id, json.photo_url, json.name, csrf_token, comment_content, object_id));
                } else {
                    let child_comment_div = $("#" + parent_id.toString()).find("#child-comments");
                    console.log(child_comment_div);
                    child_comment_div.prepend(get_child_comment_html(json.comment_id, json.photo_url, json.name, csrf_token, comment_content, object_id));
                }
                offEvents();
                setEvents();
                $(".comment-create").find("#id_content").val("");
            },

            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            },
        });
    };
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

function get_parent_comment_html(comment_id, photo_url, name, csrf_token, comment_content, object_id) {
    return `<div id="` + comment_id + `">
            <div class="row nopadding margin-bottom15 comment">
                <div class="comment-not-edited">
                    <div class="col-sm-2">
                        <img class="img-responsive img-thumbnail"
                             src="` + photo_url + `">
                    </div>
                    <div class="col-sm-10">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <strong>` + name +
        `</strong>
                                <span class="text-muted">0 minutes ago | 0
                                Odpowiedzi | <a href="#" class="comment-reply-btn">Pokaż</a> |
                                        <a href="#" class="comment-edit-btn">Edytuj</a> |
                                        <form method="POST" action="." class="comment-delete"
                                              style="display: inline;">
                                            <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
                                            <input type="hidden" name="comment_id" value="` + comment_id + `">
                                            <button type="submit" class="link">Usuń</button>
                                        </form>
                                    </span>
                            </div>
                            <div id="content` + comment_id + `"
                                 class="panel-body overflow-break-word">` + comment_content + `</div>
                        </div>
                    </div>
                </div>
                <div class="comment-edited margin-bottom-15" style="display:none;">
                    <form method="POST" action="." class="comment-edit">
                        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">            
                        <input id="id_content_type" name="content_type" type="hidden" value="post">
                        <input id="id_object_id" name="object_id" type="hidden" value="` + object_id + `">
                        <div id="div_id_content" class="form-group"> 
                            <div class="controls ">
                                <textarea class="textarea form-control form-control" cols="40" id="id_content" name="content" rows="10"></textarea>
                            </div> 
                        </div>
                        <input type="hidden" name="comment_id" value="` + comment_id + `">
                        <p id="comment-content-validation-message" class="validation-message">Komentarz nie może być pusty.</p>
                        <button type="submit" class="btn btn-default margin-bottom-15">Zapisz</button>
                    </form>
                </div>
                <div class="comment_reply" style="display: none;">
                    <div class="row nopadding margin-bottom15">
                        <div id="child-comments" class="col-sm-10 pull-right nopadding">
                            <form method="POST" action="." class="comment-create margin-bottom-15 padding-sides-15">
                                <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
                                <input id="id_content_type" name="content_type" type="hidden" value="post">
                                <input id="id_object_id" name="object_id" type="hidden" value="` + object_id + `">
                                <div id="div_id_content" class="form-group">
                                    <div class="controls ">
                                        <textarea class="textarea form-control" cols="40" id="id_content" name="content" rows="10"></textarea>
                                    </div>
                                </div>
                                <input type="hidden" name="parent_id" value="` + comment_id + `">
                                <input id="comment-user-validator" type="hidden" value="True">
                                <div id="comment-content-validation-message" class="validation-message">
                                    <p>Musisz być zalogowany aby dodawać komentarze. </p>
                                    <p class="black-color"><a href="/accounts/login/">Zaloguj </a>lub <a href="/accounts/signup/">zarejestruj się </a>
                                    jeśli nie masz jeszcze konta.</p>
                                </div>
                                <button type="submit" class="btn btn-default">Odpowiedz</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;
}

function get_child_comment_html(comment_id, photo_url, name, csrf_token, comment_content, object_id) {
    return `<div id="` + comment_id + `">
                <div class="comment-not-edited">
                    <div class="col-sm-2">
                        <img class="img-responsive img-thumbnail"
                            src="`+ photo_url + `">
                    </div>
                    <div class="col-sm-10">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <strong>` + name + `</strong>
                                <span class="text-muted">0 minutes ago |
                                    <a href="#" class="comment-edit-btn">Edytuj</a> |
                                    <form method="POST" action="." class="comment-delete" style="display: inline;">
                                        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
                                        <input type="hidden" name="comment_id" value="` + comment_id + `">
                                        <button type="submit" class="link">Usuń</button>
                                    </form>
                                </span>
                            </div>
                            <div id="content` + comment_id + `" class="panel-body overflow-break-word">` + comment_content + `</div>
                        </div>
                    </div>
                </div>
                <div class="comment-edited margin-bottom-15 padding-sides-15" style="display: none">
                    <form method="POST" action="." class="comment-edit">
                        <input type="hidden" name="csrfmiddlewaretoken" value="` + csrf_token + `">
                        <input id="id_content_type" name="content_type" type="hidden" value="post">
                        <input id="id_object_id" name="object_id" type="hidden" value="` + object_id + `">
                        <div id="div_id_content" class="form-group">
                            <div class="controls ">
                                <textarea class="textarea form-control form-control form-control" cols="40" id="id_content" name="content" rows="10"></textarea>
                            </div> 
                        </div>
                        <input type="hidden" name="comment_id" value="` + comment_id + `">
                        <p id="comment-content-validation-message" class="validation-message">Komentarz nie może być pusty.</p>
                        <button type="submit" class="btn btn-default margin-bottom-15">Zapisz</button>
                    </form>
                </div>
            </div>`;
}