$(function(){
    $("#login").click(function(){
        var name = $("#username").val()
        var psw = $("#password").val()
        if (name == "" || psw == ""){
            alert("请填写完整");
            return;
        }
        console.log("start");
        $.post("/",
               {username: name,
                password: psw
               },
               function(response, status){
                   //save cookies, redirect to home page
                   window.location.replace("/home");
               })
               .fail(function(jqXHR, textStatus, errorThrown){
                   $(".error").fadeIn(400).delay(3000).fadeOut(400); 
               });
    });
});
