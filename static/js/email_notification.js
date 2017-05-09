$(document).ready(function () {
    $("form#message-form").on('submit', function (event) {
        event.preventDefault();
        console.log("Some shit");
    });
})