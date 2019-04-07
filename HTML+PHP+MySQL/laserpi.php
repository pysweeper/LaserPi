<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";

  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

  /* check connection */
  if ($mysqli->connect_errno)
  {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
  }

 /**
  *@pre Database connection successful
  *@post Writes the header of the laserpi web page, which includes both a title header and a form which can be used to either create, start, or terminate laserpi games based on the database state
  */
  function printHeader()
  {
    global $mysqli;
    $game_state = 0;
    $game_id = 0;

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
      echo "<input type='submit' value='Create New Game'></form>";
    }
    else if ($game_state == 1)
    {
      echo "<h3>Game Open for Player(s) to Join (Game ID =  " . $game_id . ")</h3>";
      echo "<form action='startGame.php' method='POST'>";
      echo "<input type='submit' value='Start Game'></form>";
    }
    else if ($game_state == 2)
    {
      echo "<h3>Game Currently In Progress (Game ID =  " . $game_id . ")</h3>";
      echo "<form action='terminateGame.php' method='POST'>";
      echo "<input type='submit' value='Terminate Game'></form>";
    }
  }

 /**
  *@pre Database connection successful and printHeader is executed
  *@post Writes a table which displays the recorded stats of every player found in the database along with a form used to create new players
  */
  function printPlayerStats()
  {
    global $mysqli;

    echo "<br><hr><h3>Player Stats</h3>";
    echo "<table><tr><th>Player Username</th><th>Game Wins</th><th>Game Losses</th><th>Total Shots Fired</th><th>View Stats by Game</tr>";

    $query = "SELECT * FROM Players";

    if ($result = $mysqli->query($query))
    {
        /* fetch associative array */
        while ($row = $result->fetch_assoc())
        {
          if ($row['username'] != 'NULL1' and $row['username'] != 'NULL2')
          {
            echo "<tr>";
            echo "<td>" . $row['username'] . "</td>";
            echo "<td>" . $row['wins'] . "</td>";
            echo "<td>" . $row['losses'] . "</td>";
            echo "<td>" . $row['shots_fired'] . "</td>";
            echo "<td>";
            echo "<form action='gameStats.php' method='POST'>";
            echo "<input type = 'hidden' name = 'user' value = '" . $row['username'] . "' />";
            echo "<input type='submit' value='Go!'></form>";
            echo "</td></tr>";
          }
        }

        /* free result set */
        $result->free();
    }

    echo "</table><br>";

    echo "<form action='createPlayer.html' method='GET'><input type='submit' value='Register New Player'></form>";

    echo "<hr>";
  }

 /**
  *@pre Database connection successful and printPlayerStats is executed
  *@post Writes a table which displays all of the stats for each gun in the database along with a form that is used to register new guns
  */
  function printGunStats()
  {
    global $mysqli;

    echo "<h3>Gun Stats</h3>";
    echo "<table><tr><th>Gun ID</th><th>Game Wins</th><th>Game Losses</th><th>Total Shots Fired</th></tr>";

    $query = "SELECT * FROM Guns";

    if ($result = $mysqli->query($query))
    {
        /* fetch associative array */
        while ($row = $result->fetch_assoc())
        {
          if ($row['gun'] != 0)
          {
            echo "<tr>";
            echo "<td>" . $row['gun'] . "</td>";
            echo "<td>" . $row['wins'] . "</td>";
            echo "<td>" . $row['losses'] . "</td>";
            echo "<td>" . $row['shots_fired'] . "</td>";
            echo "</tr>";
          }
        }

        /* free result set */
        $result->free();
    }

    echo "</table><br>";

    echo "<form action='registerGun.php' method='POST'><input type='submit' value='Register New Gun'></form>";

    echo "<hr>";
  }

 /**
  *@pre Database connection successful and printGunStats is executed
  *@post Writes a table which contains stats on every game stored in the database
  */
  function printGameStats()
  {
    global $mysqli;

    echo "<h3>Game Stats</h3>";
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

        //If no players were in the game, write an html table row with no players
        if ($numPlayers == 0)
        {
          $query = "SELECT * FROM Games WHERE Games.id=" . $i;
          if ($result = $mysqli->query($query))
          {
            if ($row = $result->fetch_assoc())
            {
              echo "<tr>";
              echo "<td>" . $row['id'] . "</td>";
              if ($row['current_state'] == 0)
              {
                echo "<td>Finished</td>";
              }
              else if ($row['current_state'] == 1)
              {
                echo "<td>Waiting for Players to Join</td>";
              }
              else if ($row['current_state'] == 2)
              {
                echo "<td>In Progress</td>";
              }

              echo "<td>None</td>";
              echo "<td>None</td>";
              echo "<td>No Winner</td>";
              echo "<td>" . $row['game_date'] . "</td>";
              echo "</tr>";
            }

            /* free result set */
            $result->free();

          }
        }
        //Otherwise, write an html table row with player information
        else
        {
          $rowArr = array();
          while ($row = $result->fetch_assoc())
          {
            array_push($rowArr, $row);
          }

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

          $result->free();
        }
      }
    }

    echo "</table><br><hr>";
  }

  printHeader();
  printPlayerStats();
  printGunStats();
  printGameStats();

?>

