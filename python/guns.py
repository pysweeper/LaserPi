import connect

def fireShot():
  mydb = connect.connect()
  sql = "UPDATE Guns SET shots_fired = shots_fired + 1 WHERE gun = 0"
  mycursor = mydb.cursor()
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
