// Generated by CoffeeScript 1.6.2
jQuery(function() {
  var clean_view, eval_string, update_retval;

  update_retval = function(data) {
    clean_view();
    if (data.error == null) {
      return $("#retval").text(data.retval);
    } else {
      return $("#eval_error").text(data.error);
    }
  };
  clean_view = function() {
    $("#retval").text("");
    return $("#eval_error").text("");
  };
  eval_string = function() {
    var s;

    s = $("#repl_input").val();
    return $.post("/eval_string/", {
      string: s
    }, update_retval);
  };
  return $("#eval_btn").bind("click", eval_string);
});
