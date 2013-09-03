jQuery ->

    simulate_input = ->
        alert "hello"
        input_real = $("#input-val")
        input_fake = $("#display-input-val")
        input_real.focus()
        input_fake.text(input_real.val())



    $(".input").bind "click", simulate_input