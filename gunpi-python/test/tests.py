import unittest
import sys
sys.path.append('../')
import connect
from gun import Gun
from trigger import Trigger
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

if __name__ == '__main__':
    unittest.main()
