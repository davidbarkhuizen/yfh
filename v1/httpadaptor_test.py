import unittest
from datetime import date
from csvhandler import CSV

class Test_CSVHandler(unittest.TestCase):

  FILE_PATH = '/home/david/mt/mtcore/JPM.csv'

  def setUp(self):
    pass

  def test_file_exists_at_path(self):
    self.assertTrue(True)      
    
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(Test_CSVHandler)
  unittest.TextTestRunner(verbosity=2).run(suite)
