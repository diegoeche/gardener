$(function () {
  $("#create_job").click(function (event) {
    event.preventDefault();
    var url       = "/api/jobs"
    var command	  = $("#actionType").val()
    var title	  = $("#actionName").val()
    var frequency = $("#frequency").val()

    var data = {
      title: title,
      command: command,
      frequency: frequency
    }
    console.log(data)
    return $.ajax(url, {
      data       : JSON.stringify(data),
      contentType: 'application/json',
      type       : 'POST',
    }).done(function (data) {
      console.log(data)
      location.reload()
    })
  })

  $(".delete_job").click(function (event) {
    event.preventDefault();
    var id = $(this).data()["index"]
    return $.post("/api/jobs/delete/" + id).done(function (data) {
      location.reload()
    })
  })
})
