<html>
  <head>
    <title>出行策略</title>
    <script>
      function validateForm()
      {
      var a=document.forms["Form"]["start"].value;
      var b=document.forms["Form"]["end"].value;
      if (a==null || a=="",b==null || b=="")
      {
      alert("Please Fill All Required Field");
      return false;
      }
      }
    </script>
  </head>
  <body>
    <form action="/" method="post" name="Form" onsubmit="return validateForm()">
      <center>
        起点:<input type="text" name="start">
        终点:<input type="text" name="end">
        日期:<input type="date" name="date">
        <input type="submit" value="提交">
      </center>
    </form>
  </body>
</html>
