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

def dumpGuns():
  mydb = connect.connect()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM Guns")
  myresult = mycursor.fetchall()
  for x in myresult:
    print(x)

dumpGuns()
