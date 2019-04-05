<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

 /**
  *
  */
  function printGameStats()
  {
    $user = $_POST["user"];
    $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

    if ($mysqli->connect_errno)
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }

    echo "<h1>Individual Game Stats for " . $user . ":</h1><br>";

    echo "<table><tr><th>Game ID</th><th>Current State</th><th>Player Usernames</th><th>Player Gun IDs</th><th>Winner</th><th>Game Start Time</th></tr>";

    $query = "SELECT * FROM Games";
    $numGames = 0;

    //Calculate how many games are in the database
    if ($result = $mysqli->query($query))
    {
      $numGames = mysqli_num_rows($result);
    }

    for ($i = 1; $i <= $numGames; $i++)
    {
      //Select all the players for each game in a joined table
      $query = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) WHERE Games.id=" . $i;
      if ($result = $mysqli->query($query))
      {
        $numPlayers = mysqli_num_rows($result);
        if ($numPlayers > 0)
        {
          $rowArr = array();
          while ($row = $result->fetch_assoc())
          {
            array_push($rowArr, $row);
          }

          //Print only rows if the desired player played in the game
          $printRow = false;
          foreach($rowArr as $row)
          {
            if ($row['username'] == $user)
            {
              $printRow = true;
            }
          }
          if ($printRow)
          {
            echo "<tr>";
            echo "<td>" . $rowArr[0]['id'] . "</td>";
            if ($rowArr[0]['current_state'] == 0)
            {
              echo "<td>Finished</td>";
            }
            else if ($rowArr[0]['current_state'] == 1)
            {
              echo "<td>Waiting for Players to Join</td>";
            }
            else if ($rowArr[0]['current_state'] == 2)
            {
              echo "<td>In Progress</td>";
            }
            echo "<td>";
            for ($j = 0; $j < $numPlayers; $j++)
            {
              echo $rowArr[$j]['username'];
              if ($j < $numPlayers - 1)
              {
                echo ", ";
              }
            }
            echo "</td>";
            echo "<td>";
            for ($j = 0; $j < $numPlayers; $j++)
            {
              echo $rowArr[$j]['gun_id'];
              if ($j < $numPlayers - 1)
              {
                echo ", ";
              }
            }
            echo "</td>";
            if ($rowArr[0]['winner'] == 0)
            {
              echo "<td>No Winner</td>";
            }
            else
            {
              foreach($rowArr as $row)
              {
                if ($row['gun_id'] == $row['winner'])
                {
                  echo "<td>" . $row['username'] . "</td>";
                }
              }
            }

            echo "<td>" . $rowArr[0]['game_date'] . "</td>";
            echo "</tr>";
          }

          $result->free();
        }
      }
    }
    echo "</table><br><hr>";
  }

  printGameStats();

?>

