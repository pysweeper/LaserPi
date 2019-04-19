<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

 /**
  *@pre A game has been created using the create game form, and then the user submitted a start game form
  *@post Sets the previously created game to the active state in the database and redirects the user back to the laserpi homepage
  */
  function startGame()
  {
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");
    $gameid = 0;

    if ($mysqli->connect_errno)
    {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
    }

    $query = "UPDATE Games SET current_state=2 WHERE current_state=1";

    if ($mysqli->query($query))
    {
      echo "<p>Game started successfully</p>";
    }
    else
    {
      echo "<p>Error: Trouble communicating with database, no game started.</p><br>";
      echo "<a href='laserpi.php'>Return to homepage?</a>";
      exit();
    }

    echo "<a href='laserpi.html'>Return to homepage?</a>";

    header("Location: https://people.eecs.ku.edu/~b040w377/laserpi.html");
    exit();
  }

  startGame();
  
?>

