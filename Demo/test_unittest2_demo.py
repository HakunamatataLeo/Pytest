# coding:utf-8
'''

Created on 2015年9月10日

@author: laughlast
'''
import os
import sys
import copy
import unittest2
import HTMLTestRunner


def is_prime(number):
    '''return true if *number* is prime.
    '''
    if number <= 1:
        return False
    for element in range(2, number):
        if number % element == 0:
            return False
    return True


def get_next_prime(number):
    '''get the closest prime larger then *number*.
    '''
    index = number
    while True:
        index = index + 1
        if is_prime(index):
            return index
    return None


class PrimesTestsBase(unittest2.TestCase):

    u'''测试一个整数是否为素数以及求一个整数后面的下一个素数(全ok)
    '''

    _NopeMsg = '{} should be not a prime!'
    _OkMsg = '{} should be a prime!'

    @classmethod
    def setUpClass(cls):
        '''demo setUpClass: begin
        '''
        print 'begin'

    @classmethod
    def tearDownClass(cls):
        '''demo tearDownClass()
        '''
        print 'end'

    def test_is_1_prime(self):
        '''1 should not be prime!
        '''
        self.assertFalse(is_prime(1), self._NopeMsg.format(1))

    def test_is_2_prime(self):
        '''2 should be prime!
        '''
        self.assertTrue(is_prime(2), self._OkMsg.format(2))

    def test_is_3_prime(self):
        '''3 should not be prime!
        '''
        self.assertTrue(is_prime(3), self._OkMsg.format(3))

    def test_is_4_prime(self):
        '''4 should not be prime!
        '''
        self.assertFalse(is_prime(4), self._NopeMsg.format(4))

    def test_is_5_prime(self):
        '''5 should be prime!
        '''
        self.assertTrue(is_prime(5), self._OkMsg.format(5))

    def test_is_negtive_prime(self):
        '''negtive should be not prime
        '''
        for k in range(-1, -10, -1):
            self.assertFalse(is_prime(k), self._NopeMsg.format(k))


class PrimesTestsWithRunTestOverrided(PrimesTestsBase):

    u'''复写TestCase的"runTest" 方法
    '''

    def runTest(self):
        '''pass'''
        assert True


class PrimesTestsWithRunOverrided(PrimesTestsBase):

    u'''复写TestCase的"run"方法
    '''

    def run(self, result=None):
        '''overriding the "run" to set result.failfast etc'''
        if result is None:
            result = unittest2.TestResult(verbosity=2)
        result.failfast = True
        super(PrimesTestsBase, self).run(result)

    def test_is_4_prime(self):
        '''4 should not be prime!'''
        self.fail(self._NopeMsg.format(4))


class PrimesTestsWith4thFailedAsExpected(PrimesTestsBase):

    u'''复写第4个测试方法使其失败并以 "expectedFailure" 装饰包装
    '''

    # take the test failed as 'expected failures' instead of 'failed'
    @unittest2.expectedFailure
    def test_is_4_prime(self):
        '''4 should not be prime!'''
        self.fail(self._NopeMsg.format(4))


class PrimesTestsWith4thFailed(PrimesTestsBase):

    u'''复写第4个测试方法使其失败
    '''

    def test_is_4_prime(self):
        '''4 should not be prime!'''
        self.fail(self._NopeMsg.format(4))


class RunUnittestDemo(unittest2.TestCase):

    u'''测试 unittest 不同的运行测试方法
    '''

    def setUp(self):
        self.tloader = unittest2.defaultTestLoader
        self.trunner = unittest2.TextTestRunner(verbosity=2, failfast=True)

    def test_run_With4thFailed(self):
        u'''运行包含一个失败的测试方法
        '''
        tsuite = self.tloader.loadTestsFromTestCase(PrimesTestsWith4thFailed)
        tresult = self.trunner.run(tsuite)
        # unittest2.TestCase的longMessage缺省为True，在trace信息后添加用户信息
        assert self.longMessage
        assert tresult.failures[0][1].index(PrimesTestsBase._NopeMsg.format(4))
        assert not tresult.wasSuccessful()
        if self.trunner.failfast:
            assert tresult.testsRun is 4
        else:
            assert tresult.testsRun is tsuite.countTestCases()

    def test_run_With4thFailedAsExpected(self):
        u'''运行包含一个失败的并以期望失败包装装饰的测试方法
        '''
        tsuite = self.tloader.loadTestsFromTestCase(PrimesTestsWith4thFailedAsExpected)
        self.trunner.failfast = True
        tresult = self.trunner.run(tsuite)
        assert tresult.wasSuccessful()
        assert tresult.testsRun is tsuite.countTestCases()

    def test_run_WithRunTestOverrided(self):
        u'''运行包含一个runTest实现的测试方法
        '''
        # 测试案例TestCaseClass无参数实例化缺省执行其 runTest 方法
        tresult = PrimesTestsWithRunTestOverrided().run()
        assert tresult.testsRun is 1 and tresult.wasSuccessful()
        # TestLoader缺省加载 test 开头的测试方法（不包括 runTest）
        tsuite = self.tloader.loadTestsFromTestCase(PrimesTestsWithRunTestOverrided)
        tresult = self.trunner.run(tsuite)
        assert tresult.testsRun is tsuite.countTestCases() \
            and tsuite.countTestCases() is 6

    def test_run_WithRunOverrided(self):
        u'''复写TestCase类中的run(result)，通过设置result参数控制执行流程等
        '''
        tsuite = self.tloader.loadTestsFromTestCase(PrimesTestsWithRunOverrided)
        tresult = self.trunner.run(tsuite)
        assert not tresult.wasSuccessful()
        # 对应run()中result.failfast为True，跳过执行失败案例后面的两个案例执行
        assert tresult.testsRun is tsuite.countTestCases() - 2

    def test_run_verify_testsuite_runned(self):
        u'''检查测试执行后的 TestSuite 实例本身变化
        '''
        tresult = unittest2.TestResult()
        tsuite = unittest2.TestSuite([PrimesTestsBase('test_is_1_prime')])
        tsuitedcp = copy.deepcopy(tsuite)
        tsuitescp = copy.copy(tsuite)
        tsuite.run(tresult)
        assert tresult.wasSuccessful() \
            and tresult.testsRun is 1
        # 测试案例执行后，所在测试集中不再保留其实例引用（被设为None）
        assert tsuite._tests == [None] \
            and tsuite.countTestCases() is 1\
            and tsuite._removed_tests is 1
        # copy引用的非深度copy有问题
        assert tsuite == tsuitescp and tsuite is not tsuitescp
        tsuite.addTest(PrimesTestsBase('test_is_2_prime'))
        # TestSuite 以addTest添加测试案例时是在持有的测试序列后append
        with self.assertRaises(TypeError):
            # 新测试案例追加到测试序列列表中原来执行过的案例后
            assert tsuite._tests[0] is None \
                and isinstance(tsuite._tests[1], PrimesTestsBase)
            # 沿用的tsuite中原已执行案例的引用被替换为None，当然 TypeError
            tsuite(tresult)
        # deepcopy没有问题
        assert tsuitedcp.run(tresult).wasSuccessful()

    def test_run_verify_testloader(self):
        u'''验证TestLoader加载测试案例的其它方法
        '''
        import test_unittest_demo
        fullname_tm = 'test_unittest_demo.PrimesTestsBase.test_is_1_prime'
        relativename_tm = 'PrimesTestsBase.test_is_1_prime'
        tsuite1 = self.tloader.loadTestsFromName(fullname_tm)
        tsuite2 = self.tloader.loadTestsFromName(relativename_tm,
                                                 test_unittest_demo)
        tsuite3 = self.tloader.loadTestsFromNames([fullname_tm])
        tsuite4 = self.tloader.loadTestsFromNames([relativename_tm],
                                                  test_unittest_demo)
        assert tsuite1.countTestCases() == tsuite2.countTestCases()\
            == tsuite3.countTestCases() == tsuite4.countTestCases() == 1
        fullname_tc = 'test_unittest_demo.PrimesTestsBase'
        relativename_tc = 'PrimesTestsBase'
        tsuite1 = self.tloader.loadTestsFromName(fullname_tc)
        tsuite2 = self.tloader.loadTestsFromName(relativename_tc,
                                                 test_unittest_demo)
        assert tsuite1.countTestCases() == tsuite2.countTestCases() == 6

        tpath = os.path.split(os.path.realpath(__file__))[0]
        # 最简单
        tsuite1 = self.tloader.loadTestsFromName('test_unittest_demo')
        # 常用也实用
        tsuite2 = self.tloader.discover(tpath, 'test*unittest*.py')
        # 最快（不用额外导入解析）
        tsuite3 = self.tloader.loadTestsFromModule(test_unittest_demo, False)
        assert tsuite1.countTestCases() == tsuite2.countTestCases()\
            == tsuite3.countTestCases()

    def test_run_single_testmethod(self):
        u'''运行本例中其它地方没有出现的单个测试方法案例
        '''
        # tresult可为以下测试执行方法共享，注意测试结果
        tresult = unittest2.TestResult()
        assert PrimesTestsBase('test_is_1_prime').run(tresult).wasSuccessful()\
            and tresult.wasSuccessful() and tresult.testsRun is 1
        # 测试案例TestCaseClass无参数实例化缺省执行其 runTest 方法
        assert PrimesTestsWithRunTestOverrided().run(tresult).wasSuccessful()\
            and tresult.wasSuccessful() and tresult.testsRun is 2
        tsuite = unittest2.TestSuite()
        tsuite.addTest(PrimesTestsBase('test_is_1_prime'))
        # 避免直接在连续独立测试中使用上一执行过的 TestSuite 实例，参见例中另外demo方法
        tsuitecopy = copy.deepcopy(tsuite)
        tsuite.run(tresult)
        assert tresult.wasSuccessful() and tresult.testsRun is 3
        # TestSuite自调用是实现 '__call__'来内部引用run(*a,**k)
        tsuitecopy(tresult)
        assert tresult.wasSuccessful() and tresult.testsRun is 4

if __name__ == '__main__':
    tloader = unittest2.defaultTestLoader
    tpath = os.path.split(os.path.realpath(__file__))[0]
    tsuite = tloader.discover(tpath, 'test*unittest*.py')
#     trunner = unittest2.TextTestRunner(verbosity=2, failfast=True)
#     tresult = trunner.run(tsuite)
#     assert not tresult.wasSuccessful()
#     print tresult
    treport = file(tpath + '\\test_primes.html', 'wb')
    htrunner = HTMLTestRunner.HTMLTestRunner(stream=treport, verbosity=2,
                                             title='test primes and unittest',
                                             description='test primes and unittest demos report')

    htresult = htrunner.run(tsuite)
    treport.close()
    print htresult
