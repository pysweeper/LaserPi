<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");
  $gameid = 0;

  if ($mysqli->connect_errno)
  {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
  }

  $query = "INSERT INTO Games (current_state, winner, game_date) VALUES (1, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 10 MINUTE))";

  if ($mysqli->query($query))
  {
    echo "<p>New Game Successfully Initialized.</p>";
  }
  else
  {
      echo "<p>Error: Trouble communicating with database, no new game created.</p><br>";
      echo "<a href='laserpi.php'>Return to homepage?</a>";
      exit();
  }

  $query = "SELECT * FROM Games";

  if ($result = $mysqli->query($query))
  {
    while ($row = $result->fetch_assoc())
    {
      $gameid = $row['id'];
    }

    $result->free();
  }

  $query = "INSERT INTO Game_Users (game_id, gun_id, username) VALUES (" . $gameid . ", 0, 'NULL1')";

  if ($mysqli->query($query))
  {
    echo "<p>First Player Slot Created Successfully</p>";
  }

  $query = "INSERT INTO Game_Users (game_id, gun_id, username) VALUES (" . $gameid . ", 0, 'NULL2')";

  if ($mysqli->query($query))
  {
    echo "<p>Second Player Slot Created Successfully</p><br>";
  }

  echo "<a href='laserpi.php'>Return to homepage?</a>";

?>
