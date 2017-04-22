// 验证输入并提交
$(function(){
  $("button").click(function(){
    var start = $("#start").val();
    var end = $("#end").val();
    var date = $("#date").val();
    if (start == "" || end == "" || date == ""){
      alert("请填写完整表单");
      return;
    }
    $.post("/",
           {start : start,
            end : end,
            date: date},
           function(data, status){
             $("#result").html(data);
           })
  });
});

// 交换出发到达城市
$(function(){
  $("#exchange-icon").click(function(){
    var start = $("#start").val();
    var end = $("#end").val();
    $("#start").val(end);
    $("#end").val(start);
  })
});
