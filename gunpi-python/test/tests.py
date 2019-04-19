import unittest
import sys
sys.path.append('../')
import connect
import gun
import mysql.connector

class TestLaserPi(unittest.TestCase):
    def setUp(self):
        pass

    def test_connect(self):
        '''
        Test for connect.py
        Should return a mysqld object.
        '''
        testDB = connect.connect()
        self.assertIsInstance(testDB, mysql.connector.connection.MySQLConnection)
        testDB.close()

    def test_validate(self):
        '''
        Test for gun.validate()
        Should ...
        '''
        pass

if __name__ == '__main__':
    unittest.main()