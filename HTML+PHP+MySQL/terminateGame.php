<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

 /**
  *@pre a game has been started with the start game form, and then the user submits a terminate game form
  *@post Sets all active games in the database to the finished state without determining a winner. Then, the user is redirected to the laserpi homepage
  */
  function terminateGame()
  {
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

    if ($mysqli->connect_errno)
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }

    $query = "UPDATE Games SET current_state = 0 WHERE current_state <> 0";

    if ($result = $mysqli->query($query))
    {
      echo "<p>Game Successfully Terminated.</p><br>";
    }
    else
    {
        echo "<p>Error: Trouble communicating with database, game did not terminate.</p><br>";
    }

    echo "<a href='laserpi.html'>Return to homepage?</a>";

    header("Location: https://people.eecs.ku.edu/~b040w377/laserpi.html");
    exit();
  }

  terminateGame();

?>

