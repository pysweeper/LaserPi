import connect

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
          print (self.id)
          file.read(9)
          self.username = (file.readline()).rstrip("\n")
          print (self.username)
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
          print("Gun id not registered. Please go to https://people.eecs.ku.edu/~b040w377/laserpi.php to register gun.")

    def fireShot(self):
      mydb = connect.connect()
      sql = "UPDATE Guns SET shots_fired = shots_fired + 1 WHERE gun = " + str(self.id)
      mycursor = mydb.cursor()
      mycursor.execute(sql)
      mydb.commit()
      print(mycursor.rowcount, "record(s) affected")

    def joinGame(self):
      mydb = connect.connect()
      sql = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) WHERE Games.current_state = 1 AND Game_Users.gun_id = 0"
      mycursor = mydb.cursor()
      mycursor.execute(sql)
      myresult = mycursor.fetchall()
      for x in myresult:
          print (x)
      if (len(myresult) == 0):
        print("Could not find a game to join")
      elif (len(myresult) == 1):
        gameid = myresult[0][0]
        sql = "UPDATE Game_Users SET gun_id = " + str(self.id) + " WHERE gun_id = 0 AND username = 'NULL2' AND game_id = " + str(gameid)
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        sql = "UPDATE Games SET current_state = 2 WHERE current_state = 1"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
      elif (len(myresult) == 2):
        gameid = myresult[0][0]
        sql = "UPDATE Game_Users SET gun_id = " + str(self.id) + " WHERE gun_id = 0 AND username = 'NULL1' AND game_id = " + str(gameid)
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")


    def dumpGuns(self):
      mydb = connect.connect()
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM Guns")
      myresult = mycursor.fetchall()
      for x in myresult:
        print(x)

x = Gun()
x.readIDFile()
