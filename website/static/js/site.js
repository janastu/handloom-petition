(function() {
  $("#formSign").submit(function() {
    $("#sign-button").button('loading');
    $.ajax({
      "type": "POST",
      "url": "/sign",
      "data": {"name": $("#form-name").val(),
               "email": $("#form-email").val()},
      "success": function(data) {
        $("#sign-button").button('reset');
        if(data['code']) {
          $("#alert-success").alert();
          $("#alert-success").removeClass('hidden');
        }
        else {
          $("#alert-warning").alert();
          $("#alert-warning").removeClass('hidden');
        }
      },
      "error": function(data) {
        $("#sign-button").button('reset');
        //Display error alert. TODO
      }
    });
    return false;
  });

  // $.ajax({
  //   "type": "GET",
  //   "url": "/count",
  //   "success": function(data) {

  //   }
  // });
})();
