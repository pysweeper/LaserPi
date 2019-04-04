import connect
import os, datetime, time

class Gun:

    def __init__(self):
        self.id = 0
        self.username = "None"

    def readIDFile(self):
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

        self.Validate()

    def Validate(self):
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
      mydb = connect.connect()
      sql = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) WHERE Games.current_state = 1 AND Game_Users.gun_id = 0"
      mycursor = mydb.cursor()
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      if (len(myresult) == 0):
        print(str(datetime.datetime.now()), "Could not find a game to join")
        return False;
      elif (len(myresult) == 1):
        gameid = myresult[0][0]
        sql = "UPDATE Game_Users SET gun_id = " + str(self.id) + ", username='" + self.username + "' WHERE gun_id = 0 AND username = 'NULL2' AND game_id = " + str(gameid)
        mycursor.execute(sql)
        mydb.commit()
        print(str(datetime.datetime.now()), "Game_Users updated (NULL2): ", mycursor.rowcount, "record(s) affected")
        sql = "UPDATE Games SET current_state = 2 WHERE current_state = 1"
        mycursor.execute(sql)
        mydb.commit()
        print(str(datetime.datetime.now()), "Updated game state: ", mycursor.rowcount, "record(s) affected")
        return True
      elif (len(myresult) == 2):
        gameid = myresult[0][0]
        sql = "UPDATE Game_Users SET gun_id = " + str(self.id) + ", username='" + self.username + "' WHERE gun_id = 0 AND username = 'NULL1' AND game_id = " + str(gameid)
        mycursor.execute(sql)
        mydb.commit()
        print(str(datetime.datetime.now()), "Game_Users updated (NULL1): ", mycursor.rowcount, "record(s) affected")
        return True

    def checkGame(self):
      mydb = connect.connect()
      sql = "SELECT * FROM Games WHERE current_state in (1,2)"
      mycursor = mydb.cursor()
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      if (len(myresult) == 0):
        print(str(datetime.datetime.now()), "Could not find a game to join")
        return False;
      else:
        return True

    def loseGame(self):
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
