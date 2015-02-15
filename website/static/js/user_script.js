var csrftoken = $('meta[name=csrf-token]').attr('content')
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
})

$("#examineeForm").submit(function (e) {
  e.preventDefault();
  formdata = $(this).serialize();
  $.post("/user/addexaminee", formdata)
    .done(function (resp) {
      console.log(resp);
      $("#addexam-results").append(resp);
    });
});

$("#examscoreForm").submit(function (e) {
  e.preventDefault();
  formdata = $(this).serialize();
  $.post("/user/examscore", formdata)
    .done(function (resp) {
      console.log(resp);
      $("#getscore-results").html(resp);
    });
});
