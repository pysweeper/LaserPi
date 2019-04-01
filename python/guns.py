import connect

id = 0

#Read the gun id from the text file 'gunid''
try:
  file = open('gunid', 'rb+')
  file.seek(-2, 2)
  id = int(file.read(1))
  file.close()
except Exception:
  print("Gun not registered. Please open gunid.dist and follow the written instructions.")
  quit()

#Gunid 0 is reserved for the database's NULL gun
if (id == 0):
  print("Gun id cannot be 0. Please open gunid.dist and follow the written instructions.")
  quit()


def fireShot():
  mydb = connect.connect()
  sql = "UPDATE Guns SET shots_fired = shots_fired + 1 WHERE gun = " + str(id)
  mycursor = mydb.cursor()
  mycursor.execute(sql)
  mydb.commit()
  print(mycursor.rowcount, "record(s) affected")

def joinGame():
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
    sql = "UPDATE Game_Users SET gun_id = " + str(id) + " WHERE gun_id = 0 AND username = 'NULL2' AND game_id = " + str(gameid)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")
    sql = "UPDATE Games SET current_state = 2 WHERE current_state = 1"
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")
  elif (len(myresult) == 2):
    gameid = myresult[0][0]
    sql = "UPDATE Game_Users SET gun_id = " + str(id) + " WHERE gun_id = 0 AND username = 'NULL1' AND game_id = " + str(gameid)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")


def dumpGuns():
  mydb = connect.connect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM Guns")
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)

dumpGuns()
joinGame()
