$(document).ready(function(){

  var locked = 0;

  $("input[type='range']").map(function()
  {
    if(this.required)
    {
      locked = locked + 1

      $("*[type=submit]").map(function(){
        $(this).attr("disabled",true);
      });

    }

    $(this).one("click",function(e)
    {
      locked = locked - 1

      if(locked == 0)
      {
        $("*[type=submit]").map(function(){$(this).attr("disabled",false)});
      }

    })
  })

  $("*[readall]").map(function() {
      locked = locked + 1;

      $("*[type=submit]").map(function(){
        $(this).attr("disabled",true);
      });

      $(this).on("ended", function(e) {
          locked = locked - 1;

          if(locked == 0)
          {
            $("*[type=submit]").map(function(){$(this).attr("disabled",false)});
          }
      });

    }).get()
  .join();

});
