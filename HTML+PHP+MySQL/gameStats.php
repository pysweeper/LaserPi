<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

 /**
  *@pre the user has submitted a view individual game stats form
  *@post fetches all games from the database with the specified username as a player and writes each game's statistics in a table format
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
    echo "<div class='container'>";
    echo "<br><br><main role='main' class='inner cover'><h1 class='display-3'>Individual Game Stats For " . $user . ":</h1><hr></main>";

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
            echo "<div class='card'><h1 class='card-header'>Game #" . $rowArr[0]['id'] . "</h1>";
            echo "<div class='card-body'><h3 class='card-title'>";
            if ($rowArr[0]['current_state'] == 0)
            {
              echo "Finished";
            }
            else if ($rowArr[0]['current_state'] == 1)
            {
              echo "Waiting for Players to Join";
            }
            else if ($rowArr[0]['current_state'] == 2)
            {
              echo "In Progress";
            }
            echo "</h1><p class='card-text'>Players: ";
            for ($j = 0; $j < $numPlayers; $j++)
            {
              echo $rowArr[$j]['username'];
              if ($j < $numPlayers - 1)
              {
                echo ", ";
              }
            }
            echo "<br>Gun IDs: ";
            for ($j = 0; $j < $numPlayers; $j++)
            {
              echo $rowArr[$j]['gun_id'];
              if ($j < $numPlayers - 1)
              {
                echo ", ";
              }
            }
            echo "<br>Winner: ";
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
                  echo $row['username'];
                }
              }
            }

            echo "<br><br>Game Start Time: " . $rowArr[0]['game_date'];

            echo "</p></div></div><br>";
          }

          $result->free();
        }
      }
    }
    echo "</table><br><hr>";
  }

  printGameStats();

?>
