<?php

$css = file_get_contents("laserpi.css");
echo "<style>" . $css . "html, body {height: 100%;}</style>";

 /**
  *@pre the user submitted a create player form
  *@post registers a new player in the database if the posted username is not blank or a duplicate. Then, either a success or error message is printed
  */
  function createPlayer()
  {
    $username = $_POST["username"];
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

    echo "<div class='container'>";
    /* check connection */
    if ($mysqli->connect_errno)
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }
    if ($username == "")
    {
      echo "<p>Error: Player cannot have empty username<p>";
      echo "<a href='https://people.eecs.ku.edu/~b040w377/createPlayer.html'>Return to Player Registration Page?</a>";
    }
    else
    {
      $query = "INSERT INTO Players (username, wins, losses, shots_fired) VALUES ('" . $username . "', 0, 0, 0)";

      if ($mysqli->query($query))
      {
          echo "<p>New user " . $username . " created successfully.<p>";
          echo "<a href='https://people.eecs.ku.edu/~b040w377/laserpi.html'>Return to homepage?</a>";
      }
      else
      {
        echo "<p>Error: User " . $username . " already exists<p>";
        echo "<a href='https://people.eecs.ku.edu/~b040w377/createPlayer.html'>Return to Player Registration Page?</a>";
      }
    }

    /* close connection */
    $mysqli->close();

    echo "</div>";
  }

  createPlayer();

?>
