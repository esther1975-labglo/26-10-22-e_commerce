$(document).ready(function(){
    $(".like").click(function(){
        var attr_id = $(this).attr('attr_id')
        var action_url = $(this).attr('action_url')
        var that = $(this)

        $.ajax({
            url: action_url,
            type: "POST",
            data: {'attr_id': attr_id },
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            success: function (result) {
                console.log("Success")
                that.toggleClass("heart");
            },
            error: function () {
                alert("Please login");
            }
            
        });
    });
});
