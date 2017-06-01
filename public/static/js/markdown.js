$(document).ready(function () {
    $(".content-markdown").each(function () {
        var content = $(this).text()
        $(this).html(marked(content))
    })

    $(".post-detail-item img").each(function () {
        $(this).addClass("img-responsive");
    })

    var contentInput = $("#id_content")

    function setContent(value) {
        $("#preview-content").html(marked(value))
        $("#preview-content img").each(function () {
            $(this).addClass("img-responsive")
        })
    }

    setContent(contentInput.val())

    contentInput.keyup(function () {
        setContent($(this).val())
    })

    var titleInput = $("#id_title")

    function setTitle(value) {
        $("#preview-title").text(value)
    }

    setTitle(titleInput.val())

    titleInput.keyup(function () {
        setTitle($(this).val())
    })
})