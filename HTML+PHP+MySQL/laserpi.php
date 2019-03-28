<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

  $game_state = 0;
  $game_id = 0;

  /* check connection */
  if ($mysqli->connect_errno)
  {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
  }

  echo "<h1>LaserPi Laser Tag!</h1><hr>";

  $query = "SELECT * FROM Games";

  if ($result = $mysqli->query($query))
  {
      /* fetch associative array */
      while ($row = $result->fetch_assoc())
      {
        if ($row['current_state'] == 1)
        {
          $game_state = 1;
          $game_id = $row['id'];
        }
        else if ($row['current_state'] == 2)
        {
          $game_state = 2;
          $game_id = $row['id'];
        }

      }

      /* free result set */
      $result->free();
  }

  if ($game_state == 0)
  {
    echo "<h3>No Game Currently Active</h3>";
    echo "<form action='newGame.php' method='POST'>";
    echo "<input type='submit' value='Create New Game'>";
  }
  else if ($game_state == 1)
  {
    echo "<h3>Game Waiting for Player(s) to Join (Game ID =  " . $game_id . ")</h3>";
    echo "<form action='terminateGame.php' method='POST'>";
    echo "<input type='submit' value='Terminate Game'>";
  }
  else if ($game_state == 2)
  {
    echo "<h3>Game Currently In Progress (Game ID =  " . $game_id . ")</h3>";
    echo "<form action='terminateGame.php' method='POST'>";
    echo "<input type='submit' value='Terminate Game'>";
  }


?>
