jQuery ->

    render_retval = (data) ->
        $('.lines').append($ "<div class='line'><span class='caret'>>><span class='inval'>#{data.inval}</span></div>")
        outval = if 'error' of data then data.error else data.outval
        $('.lines').append($ "<div class='line'><span class='outval'>#{outval}</span></div>")

    submit_for_eval = (str) ->
        $.post '/eval_string/', string: str, render_retval

    $('#input-val').bind 'keypress', (e) ->
        if e.keyCode is 13
            submit_for_eval $(e.currentTarget).val()
            $(e.currentTarget).val('')

