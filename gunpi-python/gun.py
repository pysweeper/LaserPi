import connect
import os, time
import datetime

class Gun:
  """ The gun class handles all the gun actions,
    including interactions with the MySQL server.
    The class has no subclasses.
  """
  def __init__(self):
    """ Constructor for the Gun class.
        Postconditions: The gun will be
        active with no id and no username.
    """
    self.id = 0
    self.username = "None"
    self.mydb = connect.connect()
    self.cursor = self.mydb.cursor()
    self.url = "https://people.eecs.ku.edu/~b040w377/laserpi.html"

  def __del__(self):
    """ Destructor for the Gun class.
        Preconditions: Gun object has fallen out of scope
        Postconditions: Closes the mysql connection stored in the Gun object
    """
    self.mydb.close()

  def readIDFile(self):
    """ readIDFile
        Preconditions: gunid.dist is readable and the Gun
        class has been initialized.  All Hardware is working.
        The readIDFile seeks to read the gunid and username
        a seperate definition will then send the id and
        username to the database.
        Postconditions: The gunid and username will be read
        into the program and validated through the database.
    """
    try:
      file = open('gunid', 'r+')
      file.seek(87, 0)
      self.id = int(file.readline())
      file.read(9)
      self.username = (file.readline()).rstrip("\n")
      file.close()
    except Exception:
      print("{}: gunid file not found. Please open gunid.dist and follow the written instructions.").format(datetime.now())
      quit()
    self.validate()

  def validate(self):
    """ Validate
        Preconditions: readIDfile must have been executed
        successfully and a connection with the database established.
        Validate seeks to check the username and id obtained from the
        readIDFile with the gunid and username's in the database.
        This does not register the username and gun id, if they aren't
        registered then the username and id will not be validated.
        Postconditions: The gunid and username will be set within the
        database for record keeping.
    """
    if (self.id == 0):
      print("Gun id cannot be 0. Please open gunid.dist and follow the written instructions.")
      quit()
    sql = ("SELECT * FROM Guns "
           "WHERE gun={}").format(self.id)
    self.cursor.execute(sql)
    myresult = self.cursor.fetchall()
    if (len(myresult) == 0):
      print("Gun id not registered. Please go to {} to register a new gun.").format(self.url)
      quit()
    sql = ("SELECT * FROM Players "
           "WHERE username='{}'").format(self.username)
    self.cursor.execute(sql)
    myresult = self.cursor.fetchall()
    if (len(myresult) == 0):
      print(("Username not registered. Please go to {} to register a new player.").format(self.url))
      quit()

  def fireShot(self):
    """ fireShot
        Preconditions: a username and gunid have been established for
        the gun, a successful connection with the database
        established, and a game has been joined.
        fireShot updates the database with + 1 shot each time a shot is
        fired.
        Postconditions: The database will be updated to reflect that
        the user of the gun fired a shot.
    """
    sql = ("UPDATE Guns SET shots_fired = shots_fired + 1 "
           "WHERE gun = '{}'").format(self.id)
    self.cursor.execute(sql)
    self.mydb.commit()
    print("{}: Gun shots updated: {} record(s) affected").format(datetime.now(), self.cursor.rowcount)
    sql = "UPDATE Players SET shots_fired = shots_fired + 1 WHERE username='" + self.username + "'"
    self.cursor.execute(sql)
    self.mydb.commit()
    print("{}: Player shot updated: {} record(s) affected").format(datetime.now(), self.cursor.rowcount)

  def joinGame(self):
    """ joinGame
        Preconditions: The hardware is working properly and a
        connection to the database has been established.
        joinGame will search for an active game in the database.
        If there is a game to join, it will be joined.
        Postconditions: A game will be joined or a message will
        be displayed that there is no game to join.
    """
    sql = "SELECT * FROM Games WHERE current_state = 1"
    self.cursor.execute(sql)
    myresult = self.cursor.fetchall()
    if (len(myresult) == 0):
      print(("{}: Could not find a game to join").format(datetime.now()))
      return False
    elif (len(myresult) == 1):
      gameid = myresult[0][0]
      sql = ("INSERT INTO Game_Users (game_id, gun_id, username) "
             "VALUES ({}, {}, {})").format(gameid, self.id, self.username)
      self.cursor.execute(sql)
      self.mydb.commit()
      print(("{}: Inserted gun data: {} record(s) affected").format(datetime.now(), self.cursor.rowcount))
      return True

  def checkGame(self):
    """ checkGame
        Preconditions: A connection has been established with the
        database.
        checkGame checks the database for an active game.
        Postconditions: If there is no active game a message will be
        displayed stating such.
    """
    sql = ("SELECT * FROM Games "
           "WHERE current_state in (1,2)")
    self.cursor.execute(sql)
    myresult = self.cursor.fetchall()
    if (len(myresult) == 0):
      print("{}: Could not find a game to join").format(datetime.now())
      return False
    else:
      return True

  def loseGame(self):
    """ loseGame
        Preconditions: A game has been joined and a connection to the
        database has been established.
        loseGame updates the database, user and gun id, with a win or a
        loss and updates the other user and gunid accordingly.  The game
        will then end.
        Postconditions: The database is updated with the proper stats
        and the game is ended.
    """
    sql = ("SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) "
           "WHERE Games.current_state = 2 AND Game_Users.gun_id <> {}").format(self.id)
    self.cursor.execute(sql)
    myresult = self.cursor.fetchall()
    if (len(myresult) == 0):
      print("{}: Could not find an active game.").format(datetime.now()) 
    else:
      opponentGun = myresult[0][5]
      opponentName = myresult[0][6]
      sql = ("UPDATE Players SET losses = losses + 1 "
             "WHERE username='{}'").format(self.username)
      self.cursor.execute(sql)
      sql = ("UPDATE Players SET wins = wins + 1 "
             "WHERE username='{}'").format(opponentName)
      self.cursor.execute(sql)
      sql = ("UPDATE Guns SET losses = losses + 1 "
             "WHERE gun='{}'").format(self.id)
      self.cursor.execute(sql)
      sql = "UPDATE Guns SET wins = wins + 1 WHERE gun='" + str(opponentGun) + "'"
      self.cursor.execute(sql)
      sql = ("UPDATE Games SET winner = '{}', current_state = 0 "
             "WHERE current_state = 2").format(opponentGun)
      self.cursor.execute(sql)
      self.mydb.commit()


  def dumpGuns(self):
    """ dumpGuns
        Preconditions: A gunid and user name has been established and
        validated.
        Postcondition: The gunid will be printed to the
        console.
    """
    self.cursor.execute("SELECT * FROM Guns")
    for x in self.cursor.fetchall():
      print(x)

if __name__ == "__main__":
  x = Gun()
  x.validate()
  print("Cannot be ran directly. Run laserpi.py to start the gun program. \n"
        "Or run test/test.py to test modules.")
