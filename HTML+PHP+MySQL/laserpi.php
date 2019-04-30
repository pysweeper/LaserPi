<?php

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

    echo "<a name='laserpi'></a><nav class='navbar sticky-top'>";
    echo "<a class='navbar-brand' href='#laserpi'>LaserPi</a>";
    echo "<a class='nav-link' href='#playgame'>Play</a>";
    echo "<a class='nav-link' href='#players'>Users</a>";
    echo "<a class='nav-link' href='#guns'>Guns</a>";
    echo "<a class='nav-link' href='#games'>Games</a>";
    echo "</nav>";


    echo "<br><br>";
    echo "<main role='main' class='inner cover'><h1 class='display-3'>LaserPi</h1><p class='lead'>An infrared laser tag game that you can play anytime, anywhere</p><a name='playgame'></a><hr></main>";

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
      echo "<div class='jumbotron'>";
      echo "<h1 class='display-4'>No Game Currently Active</h1>";
      echo "<p class='lead'>Click the button below to initialize a new game and get started</p>";
      echo "<form action='newGame.php' method='POST'>";
      echo "<input type='submit' class='btn btn-light' value='Create New Game'></form></div>";
    }
    else if ($game_state == 1)
    {
      echo "<div class='jumbotron'>";
      echo "<h1 class='display-4'>Game Open for Players to Join</h1>";
      echo "<p class='lead'>Game ID =  " . $game_id . "</p><p class='lead'>Once all players have joined, click to button below to begin the game";
      echo "<form action='startGame.php' method='POST'>";
      echo "<input type='submit' class='btn btn-light' value='Start Game'></form></div>";
    }
    else if ($game_state == 2)
    {
      echo "<div class='jumbotron'>";
      echo "<h1 class='display-4'>Game Currently In Progress</h1>";
      echo "<p class='lead'>Game ID =  " . $game_id . "</p><p class='lead'>If you need to terminate the game early, click the button below";
      echo "<form action='terminateGame.php' method='POST'>";
      echo "<input type='submit' class='btn btn-light' value='Terminate Game'></form></div>";
    }
  }

 /**
  *@pre Database connection successful and printHeader is executed
  *@post Writes a table which displays the recorded stats of every player found in the database along with a form used to create new players
  */
  function printPlayerStats()
  {
    global $mysqli;

    echo "<a name='players'></a><hr><br><br><h1 class='display-4'>Player Stats</h1><br>";

    $query = "SELECT * FROM Players";

    if ($result = $mysqli->query($query))
    {
        /* fetch associative array */
        while ($row = $result->fetch_assoc())
        {
          if ($row['username'] != 'NULL1' and $row['username'] != 'NULL2')
          {
            echo "<div class='card'><h1 class='card-header'>" . $row['username'] . "</h1>";
            echo "<div class='card-body'><h3 class='card-title'>" . ($row['wins'] + $row['losses']) . " Games Played</h3>";
            echo "<p class='card-text'> " . $row['wins'] . " Games Won<br>";
            echo $row['losses'] . " Games Lost<br>";
            echo $row['shots_fired'] . " Shots Fired<br><br>";
            echo number_format(($row['wins'] / ($row['wins'] + $row['losses']) * 100), 2) . "% Winrate<br>";
            echo "<form action='gameStats.php' method='POST'>";
            echo "<input type = 'hidden' name = 'user' value = '" . $row['username'] . "' />";
            echo "<input type='submit' class='btn btn-light' value='View Individual Game Stats'></form>";
            echo "</div></div><br>";
          }
        }

        /* free result set */
        $result->free();
    }

    echo "<a name='guns'></a><form action='createPlayer.html' method='GET'><input type='submit' class='btn btn-light' value='Register New Player'></form>";

    echo "<hr>";
  }

 /**
  *@pre Database connection successful and printPlayerStats is executed
  *@post Writes a table which displays all of the stats for each gun in the database along with a form that is used to register new guns
  */
  function printGunStats()
  {
    global $mysqli;

    echo "<h1 class='display-4'>Gun Stats</h1><br>";

    $query = "SELECT * FROM Guns";

    if ($result = $mysqli->query($query))
    {
        /* fetch associative array */
        while ($row = $result->fetch_assoc())
        {
          if ($row['gun'] != 0)
          {
            echo "<div class='card'><h1 class='card-header'>Gun #" . $row['gun'] . "</h1>";
            echo "<div class='card-body'><h3 class='card-title'>" . ($row['wins'] + $row['losses']) . " Games Played</h3>";
            echo "<p class='card-text'> " . $row['wins'] . " Games Won<br>";
            echo $row['losses'] . " Games Lost<br>";
            echo $row['shots_fired'] . " Shots Fired<br><br>";
            echo number_format(($row['wins'] / ($row['wins'] + $row['losses']) * 100), 2) . "% Winrate<br>";
            echo "</div></div><br>";
          }
        }

        /* free result set */
        $result->free();
    }

    echo "</table><br>";

    echo "<a name='games'></a><form action='registerGun.php' method='POST'><input type='submit' class='btn btn-light' value='Register New Gun'></form>";

    echo "<hr>";
  }

 /**
  *@pre Database connection successful and printGunStats is executed
  *@post Writes a table which contains stats on every game stored in the database
  */
  function printGameStats()
  {
    global $mysqli;

    echo "<h1 class='display-4'>Game Stats</h1><br>";

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
              echo "<div class='card'><h1 class='card-header'>Game #" . $row['id'] . "</h1>";
              echo "<div class='card-body'><h3 class='card-title'>";
              if ($row['current_state'] == 0)
              {
                echo "Finished";
              }
              else if ($row['current_state'] == 1)
              {
                echo "Waiting for Players to Join";
              }
              else if ($row['current_state'] == 2)
              {
                echo "In Progress";
              }
              echo "</h3><p class='card-text'>Players: None<br>Gun IDs: None<br> Winner: No Winner<br><br>Game Start Time: " . $row['game_date'];
              echo "</p></div></div><br>";
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

          $result->free();
        }
      }
    }

    echo "<br><hr>";
  }

  printHeader();
  printPlayerStats();
  printGunStats();
  printGameStats();

?>
