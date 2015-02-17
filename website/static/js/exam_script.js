$(function() {
  $("#startexam").click(function () {
    $("#exam-body").show();
    $("#top-panel").slideUp("slow");
    $("#listening").trigger("play");
    setInterval(function() {
      $.post("/exam/update_results", $("form").serializeArray());
    }, 1000 * 60 * 5);
  });
});
