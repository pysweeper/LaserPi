<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

  if ($mysqli->connect_errno)
  {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
  }

  $query = "INSERT INTO Games (current_state, winner) VALUES (1, 0)";

  if ($result = $mysqli->query($query))
  {
    echo "<p>New Game Successfully Initialized.</p><br>";
  }
  else
  {
      echo "<p>Error: Trouble communicating with database, no new game created.</p><br>";
  }

  echo "<a href='laserpi.php'>Return to homepage?</a>";

?>
