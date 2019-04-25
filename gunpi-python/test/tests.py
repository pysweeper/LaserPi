import unittest
import sys
sys.path.append('../')
import connect
from gun import Gun
from led import LED
import mysql.connector

class TestLaserPi(unittest.TestCase):
    def setUp(self):
        pass

    def test_connectReturnsInstanceOfMySQLConnection(self):
      testDB = connect.connect()
      self.assertIsInstance(testDB, mysql.connector.connection.MySQLConnection)
      testDB.close()

    def test_readIDFileAssignsCorrectValuesFromProperlyFormattedFile(self):
      file = open('gunid', 'r+')
      file.write("# User Identification File.\n# Change gunid and username.\n# Rename file to gunid.\ngunid=3\nusername=Benjamin\n")
      file.close()
      gun = Gun()
      gun.readIDFile()
      self.assertEqual(gun.id, 3)
      self.assertEqual(gun.username, "Benjamin")

	def test_LEDIsToggling
	  led = LED()
	  print(led.toggleLED('green'))

if __name__ == '__main__':
    unittest.main()
