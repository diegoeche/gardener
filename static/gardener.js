$(function () {
  $("#test_positions").click( function() {
    var button = $(this);
    var oldHtml = button.html();
    button.html("Waiting...");
    $.post("/gardener/test_move").done(function (response) {
      console.log(response);
      button.html(oldHtml);
    })
    console.log("Button clicked!");
  });
  console.log("Setting up");
})
