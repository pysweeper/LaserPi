<?php

/**
 *
 */
 function registerGun()
 {
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

    if ($mysqli->connect_errno)
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }

    $query = "INSERT INTO Guns (wins, losses, shots_fired) VALUES (0, 0, 0)";

    if ($mysqli->query($query))
    {
      echo "<p>New gun successfully registered.<p>";

      $query = "SELECT * FROM Guns ORDER BY gun DESC LIMIT 1";

      if ($result = $mysqli->query($query))
      {
          /* fetch associative array */
          while ($row = $result->fetch_assoc())
          {
            echo "<p>Your gun id is: " . $row['gun'] . "</p>";
          }

          /* free result set */
          $result->free();
      }

      echo "<a href='https://people.eecs.ku.edu/~b040w377/laserpi.html'>Return to homepage?</a>";
      header("Location: https://people.eecs.ku.edu/~b040w377/laserpi.html");
      exit();
    }
    else
    {
      echo "<p>Error: Trouble registering new gun.<p>";
      echo "<a href='https://people.eecs.ku.edu/~b040w377/laserpi.html'>Return to homepage?</a>";
    }
  }

  registerGun();

?>

