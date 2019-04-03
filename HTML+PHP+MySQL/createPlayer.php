<?php
  $username = $_POST["username"];
  $mysqli = new mysqli("mysql.eecs.ku.edu", "b040w377", "Uefai3Ai", "b040w377");

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

?>
