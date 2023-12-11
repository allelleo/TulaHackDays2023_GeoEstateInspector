$(document).ready(function() {
    $('.message a').click(function(){
        $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
    });
});


$(document).ready(function () {
    $('.input-file input[type=file]').on('change', function(){
      let file = this.files[0];
      $(this).closest('.input-file').find('.input-file-text').html(file.name);
    });
  });