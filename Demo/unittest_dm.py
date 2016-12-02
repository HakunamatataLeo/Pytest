# -*- coding = utf-8 -*-

import unittest
from HTMLTestRunner import HTMLTestRunner
def fun(x):
    	return x+1

class Mytest(unittest.TestCase):

    def test_one(self):
    	self.assertEqual(fun(3),4)
    
    def test_two(self):
    	self.assertEqual(fun(2),3)

'''if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Mytest("test_one"))
    print 'One'
    suite.addTest(Mytest("test_two"))
    print 'Two'
    runner = unittest.TextTestRunner()
    runner.run(suite)
'''
if __name__ == '__main__':
    testsuit = unittest.TestSuite()
    testsuit.addTest(Mytest("test_one")) 
    testsuit.addTest(Mytest("test_two")) 
    with open('./report.html','wb') as fp:
         runner = HTMLTestRunner(stream = fp,
                                 title = 'TestReport',
                                 description = 'Result')
         runner.run(testsuit)

