import connect
import os, datetime, time

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
    #Read the gun id from the text file 'gunid'
    try:
      file = open('gunid', 'r+')
      file.seek(87, 0)
      self.id = int(file.readline())
      file.read(9)
      self.username = (file.readline()).rstrip("\n")
      file.close()
    except Exception:
      print("gunid file not found. Please open gunid.dist and follow the written instructions.")
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
    #Gunid 0 is reserved for the database's NULL gun
    if (self.id == 0):
      print("Gun id cannot be 0. Please open gunid.dist and follow the written instructions.")
      quit()
    mydb = connect.connect()
    sql = "SELECT * FROM Guns WHERE gun=" + str(self.id)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
      print("Gun id not registered. Please go to https://people.eecs.ku.edu/~b040w377/laserpi.html to register a new gun.")
      quit()
    sql = "SELECT * FROM Players WHERE username='" + self.username + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
      print("Username not registered. Please go to https://people.eecs.ku.edu/~b040w377/laserpi.html to register a new player.")
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
    mydb = connect.connect()
    sql = "UPDATE Guns SET shots_fired = shots_fired + 1 WHERE gun = " + str(self.id)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    print(str(datetime.datetime.now()), "Gun shots updated: ", mycursor.rowcount, "record(s) affected")
    sql = "UPDATE Players SET shots_fired = shots_fired + 1 WHERE username='" + self.username + "'"
    mycursor.execute(sql)
    mydb.commit()
    print(str(datetime.datetime.now()), "Player shot updated: ", mycursor.rowcount, "record(s) affected")

  def joinGame(self):
    """ joinGame
        Preconditions: The hardware is working properly and a 
        connection to the database has been established.
        joinGame will search for an active game in the database.
        If there is a game to join, it will be joined.
        Postconditions: A game will be joined or a message will
        be displayed that there is no game to join.
    """
    mydb = connect.connect()
    sql = "SELECT * FROM Games WHERE current_state = 1"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
      print(str(datetime.datetime.now()), "Could not find a game to join")
      return False
    elif (len(myresult) == 1):
      gameid = myresult[0][0]
      sql = "INSERT INTO Game_Users (game_id, gun_id, username) VALUES ("+str(gameid)+", "+str(self.id)+", '"+self.username+"')"
      mycursor.execute(sql)
      mydb.commit()
      print(str(datetime.datetime.now()), "Inserted gun data: ", mycursor.rowcount, "record(s) affected")
      return True

  def checkGame(self):
    """ checkGame
        Preconditions: A connection has been established with the 
        database.
        checkGame checks the database for an active game.
        Postconditions: If there is no active game a message will be 
        displayed stating such.
    """
    mydb = connect.connect()
    sql = "SELECT * FROM Games WHERE current_state in (1,2)"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
      print(str(datetime.datetime.now()), "Could not find a game to join")
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
    mydb = connect.connect()
    sql = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) WHERE Games.current_state = 2 AND Game_Users.gun_id <> " + str(self.id)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if (len(myresult) == 0):
      print(str(datetime.datetime.now()), "Could not find an active game.")
    else:
      opponentGun = myresult[0][5]
      opponentName = myresult[0][6]
      sql = "UPDATE Players SET losses = losses + 1 WHERE username='" + self.username + "'"
      mycursor.execute(sql)
      sql = "UPDATE Players SET wins = wins + 1 WHERE username='" + opponentName + "'"
      mycursor.execute(sql)
      sql = "UPDATE Guns SET losses = losses + 1 WHERE gun='" + str(self.id) + "'"
      mycursor.execute(sql)
      sql = "UPDATE Guns SET wins = wins + 1 WHERE gun='" + str(opponentGun) + "'"
      mycursor.execute(sql)
      sql = "UPDATE Games SET winner = " + str(opponentGun) + ", current_state = 0 WHERE current_state = 2"
      mycursor.execute(sql)
      mydb.commit()


  def dumpGuns(self):
    """ dumpGuns
        Preconditions: A gunid and user name has been established and 
        validated.
        Postcondition: The gunid will be printed to the 
        console.
    """
    mydb = connect.connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Guns")
    myresult = mycursor.fetchall()
    for x in myresult:
      print(x)

if __name__ == "__main__":
  x = Gun()
  x.readIDFile()
  x.joinGame()
  x.loseGame()
