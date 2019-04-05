<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

 /**
  *
  */
  function createGame()
  {
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");
    $gameid = 0;

    if ($mysqli->connect_errno)
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }

    $query = "INSERT INTO Games (current_state, winner, game_date) VALUES (1, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))";

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

    echo "<a href='laserpi.html'>Return to homepage?</a>";

    header("Location: https://people.eecs.ku.edu/~b040w377/laserpi.html");
    exit();
  }

  createGame();
  
?>

