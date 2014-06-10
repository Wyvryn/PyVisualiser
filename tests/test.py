'''
Created on Nov 7, 2013

@author: Mike
'''
import unittest
import src.main as main
import src.process as process


class Test(unittest.TestCase):


    def testProcInit(self):
        p = process.Process()
        self.assertEquals(0, p.Time)
        self.assertEquals(0, p.frameRate)
        self.assertEquals(0, p.signal)
    
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()