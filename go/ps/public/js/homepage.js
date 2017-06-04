$(function(){
    $("#search").click(function(){
        var pname = $("#pname").val();
        if (pname == "") {
            alert("进程名不能为空");
        }
        $.post(
            "/home",
            {pname: pname},
            function(response, status){
                $("#result-container").html(response);
                console.log(response);
            })
            .fail(function(jqXHR, textStatus, errThrow){
                console.log(textStatus);
            });
    });
});
