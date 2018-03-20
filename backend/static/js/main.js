$(function(){
    $(".heading-compose").click(function() {
      $(".side-two").css({
        "left": "0"
      });
    });

    $(".sideBar-body").click(function() {
      $(".side-two").css({
        "left": "-100%"
      });
    });
})