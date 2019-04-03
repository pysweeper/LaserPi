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
    echo "<input type='submit' value='Create New Game'></form>";
  }
  else if ($game_state == 1)
  {
    echo "<h3>Game Waiting for Player(s) to Join (Game ID =  " . $game_id . ")</h3>";
    echo "<form action='terminateGame.php' method='POST'>";
    echo "<input type='submit' value='Terminate Game'></form>";
  }
  else if ($game_state == 2)
  {
    echo "<h3>Game Currently In Progress (Game ID =  " . $game_id . ")</h3>";
    echo "<form action='terminateGame.php' method='POST'>";
    echo "<input type='submit' value='Terminate Game'></form>";
  }

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

  echo "<h3>Game Stats</h3>";
  echo "<table><tr><th>Game ID</th><th>Current State</th><th>Player 1's Username</th><th>Player 1's Gun ID</th><th>Player 2's Username</th><th>Player 2's Gun ID</th><th>Winner</th><th>Game Start Time</th></tr>";

  $query = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id)";

  if ($result = $mysqli->query($query))
  {
      /* fetch associative array */
      while ($row = $result->fetch_assoc())
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
        if ($row['username'] == 'NULL1' or $row['username'] == 'NULL2')
        {
          echo "<td>None</td>";
        }
        else
        {
          echo "<td>" . $row['username'] . "</td>";
        }
        echo "<td>" . $row['gun_id'] . "</td>";

        $player1 = $row['username'];
        $player1Gun = $row['gun_id'];

        $row = $result->fetch_assoc();
        if ($row['username'] == 'NULL1' or $row['username'] == 'NULL2')
        {
          echo "<td>None</td>";
        }
        else
        {
          echo "<td>" . $row['username'] . "</td>";
        }
        echo "<td>" . $row['gun_id'] . "</td>";
        if ($row['winner'] == 0)
        {
          echo "<td>No Winner</td>";
        }
        else
        {
          if ($row['winner'] == $player1Gun)
          {
            echo "<td>" . $player1 . "</td>";
          }
          else
          {
            echo "<td>" . $row['username'] . "</td>";
          }

        }
        echo "<td>" . $row['game_date'] . "</td>";
        echo "</tr>";
      }

      /* free result set */
      $result->free();
  }

  echo "</table><br><hr>";


?>

