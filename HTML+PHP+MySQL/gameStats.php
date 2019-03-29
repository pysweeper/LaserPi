<?php
  $css = file_get_contents("laserpi.css");
  echo "<style>" . $css . "</style>";
  $user = $_POST["user"];
  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

  if ($mysqli->connect_errno)
  {
      printf("Connect failed: %s\n", $mysqli->connect_error);
      exit();
  }

  echo "<h3>Individual Game Stats for " . $user . ":";

  echo "<table><tr><th>Game ID</th><th>Current State</th><th>Player 1's Username</th><th>Player 1's Gun ID</th><th>Player 2's Username</th><th>Player 2's Gun ID</th><th>Winner's Gun ID</th><th>Game Start Time</th></tr>";

  $query = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id)";

  if ($result = $mysqli->query($query))
  {
      /* fetch associative array */
      while ($row = $result->fetch_assoc())
      {
        $previousRow = $row;
        $row = $result->fetch_assoc();
        if ($previousRow['username'] == $user or $row['username' == $user])
        {
          echo "<tr>";
          echo "<td>" . $previousRow['id'] . "</td>";
          if ($previousRow['current_state'] == 0)
          {
            echo "<td>Finished</td>";
          }
          else if ($previousRow['current_state'] == 1)
          {
            echo "<td>Waiting for Players to Join</td>";
          }
          else if ($previousRow['current_state'] == 2)
          {
            echo "<td>In Progress</td>";
          }
          if ($previousRow['username'] == 'NULL1' or $previousRow['username'] == 'NULL2')
          {
            echo "<td>None</td>";
          }
          else
          {
            echo "<td>" . $previousRow['username'] . "</td>";
          }
          echo "<td>" . $previousRow['gun_id'] . "</td>";

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
            echo "<td>" . $row['winner'] . "</td>";
          }
          echo "<td>" . $row['game_date'] . "</td>";
          echo "</tr>";
        }
      }

      /* free result set */
      $result->free();
  }

  echo "</table><br><hr>";
?>
