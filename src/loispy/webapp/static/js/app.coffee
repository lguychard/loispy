jQuery ->

    update_retval = (data) ->
        clean_view()
        if not data.error?
            $("#retval").text data.retval
        else
            $("#eval_error").text data.error

    clean_view = ->
        $("#retval").text ""
        $("#eval_error").text ""

    eval_string = ->
        s = $("#repl_input").val()
        $.post "/eval_string/", string:s, update_retval

    $("#eval_btn").bind "click", eval_string

