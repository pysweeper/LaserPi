import unittest
import sys
sys.path.append('../')
import connect
from gun import Gun
import mysql.connector

class TestLaserPi(unittest.TestCase):
    def setUp(self):
        pass

    def test_connectReturnsInstanceOfMySQLConnection(self):
      testDB = connect.connect()
      self.assertIsInstance(testDB, mysql.connector.connection.MySQLConnection)
      testDB.close()

    def test_readIDFileReturnsFalseFromPoorlyFormattedFile(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("not a good file")
      file.close()
      gun = Gun()
      self.assertFalse(gun.readIDFile())

    def test_readIDFileAssignsCorrectValuesFromProperlyFormattedFile(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()
      self.assertEqual(gun.id, 3)
      self.assertEqual(gun.username, "Benjamin")

    def test_validateReturnsFalseWhenIdIs0(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=0\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      self.assertFalse(gun.readIDFile())

    def test_validateReturnsFalseWhenGunIsNotRegistered(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=-1\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      self.assertFalse(gun.readIDFile())

    def test_validateReturnsFalseWhenPlayerIsNotRegistered(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=None\n")
      file.close()
      gun = Gun()
      self.assertFalse(gun.readIDFile())

    def test_validateReturnsTrueWhenInputIsProperlyFormatted(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      self.assertTrue(gun.readIDFile())

    def test_fireShotCorrectlyIncrementsGunShotsFiredInDatabase(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = ("SELECT * FROM Guns "
            "WHERE gun='{}'").format(gun.id)
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldShots = myresult[0][3]

      gun.fireShot()

      sql = ("SELECT * FROM Guns "
            "WHERE gun='{}'").format(gun.id)
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newShots = myresult[0][3]

      mydb.close()
      self.assertEqual((oldShots + 1), newShots)

    def test_fireShotCorrectlyIncrementsPlayerShotsFiredInDatabase(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = ("SELECT * FROM Players "
            "WHERE username='{}'").format(gun.username)
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldShots = myresult[0][3]

      gun.fireShot()

      sql = ("SELECT * FROM Players "
            "WHERE username='{}'").format(gun.username)
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newShots = myresult[0][3]

      mydb.close()
      self.assertEqual((oldShots + 1), newShots)

    def test_joinGameReturnsFalseWhenThereIsNoActiveGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()
      self.assertFalse(gun.joinGame())

    def test_joinGameReturnsTrueWhenThereIsAnActiveGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (1, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      self.assertTrue(gun.joinGame())

      sql = "UPDATE Games SET current_state=0 WHERE current_state=1"
      cursor.execute(sql)
      mydb.commit()

      mydb.close()

    def test_joinGameCorrectlyAddsUserIntoGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (1, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      gun.joinGame()

      sql = "SELECT * FROM (Games INNER JOIN Game_Users ON Games.id = Game_Users.game_id) WHERE Games.current_state = 1"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      self.assertEqual(len(myresult), 1) #only one row added to database
      self.assertEqual(myresult[0][5], 3) #gunid is 3
      self.assertEqual(myresult[0][6], "Benjamin") #username is Benjamin

      sql = "UPDATE Games SET current_state=0 WHERE current_state=1"
      cursor.execute(sql)
      mydb.commit()

      mydb.close()

    def test_checkGameReturnsFalseWhenThereIsNoActiveGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()
      self.assertFalse(gun.checkGame())

    def test_checkGameReturnsTrueWhenThereIsAJoiningGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (1, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      self.assertTrue(gun.checkGame())

      sql = "UPDATE Games SET current_state=0 WHERE current_state=1"
      cursor.execute(sql)
      mydb.commit()

      mydb.close()
    
    def test_checkGameReturnsTrueWhenThereIsAnActiveGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (2, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      self.assertTrue(gun.checkGame())

      sql = "UPDATE Games SET current_state=0 WHERE current_state=2"
      cursor.execute(sql)
      mydb.commit()

      mydb.close()

    def test_loseGameReturnsFalseWhenThereIsNoActiveGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      self.assertFalse(gun.loseGame())

    def test_loseGameReturnsFalseWhenThereIsNoOpponentInGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (2, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      gun.joinGame()

      self.assertFalse(gun.loseGame())

      sql = "UPDATE Games SET current_state=0 WHERE current_state=2"
      cursor.execute(sql)
      mydb.commit()

      mydb.close()

    def test_loseGameReturnsTrueWhenThereIsAnOpponentInGame(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=4\nusername=Thomas\n")
      file.close()
      gun2 = Gun()
      gun2.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (2, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      gun.joinGame()
      gun2.joinGame()

      self.assertTrue(gun2.loseGame())

      mydb.close()

    def test_loseGameCorrectlyUpdatesLoserStats(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=4\nusername=Thomas\n")
      file.close()
      gun2 = Gun()
      gun2.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (2, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      sql = "SELECT * FROM Guns WHERE gun=4"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldGunLosses = myresult[0][2]

      sql = "SELECT * FROM Players WHERE username='Thomas'"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldPlayerLosses = myresult[0][2]

      gun.joinGame()
      gun2.joinGame()
      gun2.loseGame()

      sql = "SELECT * FROM Guns WHERE gun=4"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newGunLosses = myresult[0][2]

      sql = "SELECT * FROM Players WHERE username='Thomas'"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newPlayerLosses = myresult[0][2]

      self.assertEqual((oldGunLosses + 1), newGunLosses)
      self.assertEqual((oldPlayerLosses + 1), newPlayerLosses)

      mydb.close()

    def test_loseGameCorrectlyUpdatesWinnerStats(self):
      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()

      file = open('gunid', 'r+')
      file.truncate()
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=4\nusername=Thomas\n")
      file.close()
      gun2 = Gun()
      gun2.readIDFile()

      mydb = connect.connect()
      cursor = mydb.cursor()
      sql = "INSERT INTO Games (current_state, winner, game_date) VALUES (2, 0, (NOW() - INTERVAL 4 HOUR + INTERVAL 11 MINUTE - INTERVAL 22 SECOND))"
      cursor.execute(sql)
      mydb.commit()

      sql = "SELECT * FROM Guns WHERE gun=3"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldGunWins = myresult[0][1]

      sql = "SELECT * FROM Players WHERE username='Benjamin'"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      oldPlayerWins = myresult[0][1]

      gun.joinGame()
      gun2.joinGame()
      gun2.loseGame()

      sql = "SELECT * FROM Guns WHERE gun=3"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newGunWins = myresult[0][1]

      sql = "SELECT * FROM Players WHERE username='Benjamin'"
      cursor.execute(sql)
      myresult = cursor.fetchall()
      newPlayerWins = myresult[0][1]

      self.assertEqual((oldGunWins + 1), newGunWins)
      self.assertEqual((oldPlayerWins + 1), newPlayerWins)

      mydb.close()

if __name__ == '__main__':
    unittest.main()
