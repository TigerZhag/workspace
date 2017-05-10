// javascript for index.html
// 显示时钟
$(function(){
  setInterval(function(){
    var date = new Date();
    var now = date.getHours() + ":" + checkTime(date.getMinutes()) + ":" + checkTime(date.getSeconds());
    $("#current-time").html(now);
  }, 1000);
});
function checkTime(i){
  if(i<10){
    i = "0" + i;
  }
  return i;
}

//桌面item点击事件
$(function(){
  $(".desktop-item").dblclick(function(){
    // 加载文章目录
    $("#show").show();
  })
});

// 最小化
$(function(){
  $("#show #show-mini").click(function(){
    $("#show").hide();
  })
});

// 最大化/还原
$(function(){
  $("#show #show-max").click(function(){
    var show = $("#show");
    console.log("width: " + show.width() + " height:" + show.height());
    if(show.width() < $(window).width()){
      show.animate({width: '100%', height: '95%', margin: '0 auto'}, 500);
    }else {
      show.animate({width: '50%', height: '90%', margin: '10 auto'}, 500);
    }
  })
});
