import mysql.connector

def connect():
  mydb = mysql.connector.connect(
    host="mysql.eecs.ku.edu",
    user="b040w377",
    passwd="Uefai3Ai",
    database="b040w377"
  )
  return mydb

if __name__ == '__main__':
  mydb = connect()
  print(mydb)
