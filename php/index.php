<html>
  <head>
    <title>php test</title>
    <meta charset="utf-8"/>
  </head>

  <body>
    <?php
      $servername = "localhost";
      $username = "tiger";
      $password = "123456";

      try {
        $conn = new PDO("mysql:host=$servername;dbname=chunlv", $username, $password);
        // set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        echo "Connected successfully";
      }
      catch(PDOException $e)
      {
        echo "Connection failed: " . $e->getMessage();
      }
?>
  </body>
</html>
