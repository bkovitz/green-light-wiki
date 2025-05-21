from teest import *

setUpCount = 0
tearDownCount = 0


class TestException(Exception):
    pass


class DidntGetException(Exception):
    pass


class ut_SomeClass:

    def __init__(self):
        # print "ut_SomeClass init"
        pass

    def testBlah(self):
        TEST_EQ("a", "a")

    def _raise(self):
        raise TestException()

    def testTestExc(self):
        TEST_EXC(TestException, self._raise)

    def _dontRaise(self):
        pass

    def testTestExcFail(self):
        try:
            TEST_EXC(TestException, self._dontRaise)
            raise DidntGetException()
        except TestFailed:
            pass

    def _raiseWithArgs(self, a, b, c):
        if a == 1 and b == 2 and c == 3:
            raise TestException()

    def testTestExcWithArgs(self):
        TEST_EXC(TestException, self._raiseWithArgs, 1, 2, 3)

    def testTestExcWithArgsFail(self):
        try:
            TEST_EXC(TestException, self._raiseWithArgs, 1, 2, 0)
            raise DidntGetException()
        except TestFailed:
            pass

    def testTestExcWithWrongNumberOfArgs(self):
        try:
            TEST_EXC(TestException, self._raiseWithArgs, 1, 2)
            TEST(0)
        except TypeError:
            pass


class ut_ClassWithSetUpAndTearDown:

    def setUp(self):
        global setUpCount
        setUpCount += 1

    def tearDown(self):
        global tearDownCount
        tearDownCount += 1

    def testThis1(self):
        TEST_EQ(1, setUpCount)
        TEST_EQ(0, tearDownCount)

    def testThis2(self):
        TEST_EQ(2, setUpCount)
        TEST_EQ(1, tearDownCount)
