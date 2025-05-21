import sys, os, os.path, re
import importlib.util
from time import time
from traceback import extract_tb, format_list

from Helpers import cmp, apply

showTimings = None
timingsLimit = None

# # We need this because Python 3 doesn't have cmp
# def cmp(a, b):
#     return (a > b) - (a < b)

# # We need this because Python 3 doesn't have apply
# def apply(func, args, kwargs=None):
#     return func(*args) if kwargs is None else func(*args, **kwargs)


class TestFailed(Exception):
    def __init__(self, message=""):
        self.message = message
        if self.message != "":
            self.message += "\n"

    def __str__(self):
        return self.message


def TEST(expr):
    if not expr:
        raise TestFailed()


def TEST_EQ(expr1, expr2):
    if expr1 != expr2:
        raise (TestFailed(repr(expr1) + " != " + repr(expr2)))


def TEST_NE(expr1, expr2):
    if expr1 == expr2:
        raise (TestFailed(repr(expr1) + " == " + repr(expr2)))


def TEST_EXC(exc, expr, *args):
    try:
        apply(expr, args)
        raise TestFailed("didn't get exception " + exc.__name__)
    except exc:
        pass


class TestRunner:

    def __init__(self, fileNames):
        self.homeDir = os.getcwd()
        self.numTests = 0
        self.numFailedTests = 0
        self._timings = []

        print("-" * 50 + " UNIT TESTS")
        for fileName in fileNames:
            self._runAllTestsInOneFile(fileName)

        print("\n")
        if self.numFailedTests == 0:
            print("All tests PASSED %s." % self._numTestsRun())
        else:
            print(
                "%d %s FAILED %s."
                % (
                    self.numFailedTests,
                    self._testWord(self.numFailedTests),
                    self._numTestsRun(),
                )
            )

    def _timingsString(self):
        result = ""
        count = 0
        for timing in self._timings:
            result += "%-50s %f\n" % timing
            count += 1
            if timingsLimit is not None and count >= timingsLimit:
                break

        return result

    def timingsByTime(self):
        self._timings.sort(lambda a, b: cmp(b[1], a[1]))
        return self._timingsString()

    def timingsByName(self):
        self._timings.sort(lambda a, b: cmp(a[0], b[0]))
        return self._timingsString()

    def _runAllTestsInOneFile(self, fileName):
        moduleName = self._stripSuffix(fileName)
        spec = importlib.util.spec_from_file_location(moduleName, moduleName + ".py")
        if spec is None:
            raise ImportError(f"Cannot find module {moduleName}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # spec = importlib.util.spec_from_file_location("utVersionedFile2", file_path)
        # module = importlib.util.module_from_spec(spec)

        for testClass in self._allTestClasses(module):
            for testFunc in self._allTestFuncs(testClass):
                if showTimings:
                    self._timeTest(testClass, testFunc)
                else:
                    self._runTest(testClass, testFunc)

    def _runTest(self, testClass, testFunc):
        obj = testClass()
        sys.stdout.write(".")
        self.numTests += 1

        if "setUp" in dir(obj):
            obj.setUp()

        try:
            testFunc(obj)
        except Exception as exc:
            print("\n\nFAILED: %s.%s" % (testClass.__name__, testFunc.__name__))
            self._printStackTrace(sys.exc_info()[2])
            print("    " + self._exceptionMsg(exc))
            self.numFailedTests += 1

        if "tearDown" in dir(obj):
            obj.tearDown()

    def _timeTest(self, testClass, testFunc):
        startTime = time()
        self._runTest(testClass, testFunc)
        endTime = time()
        self._timings.append(
            ("%s:%s" % (testClass.__name__, testFunc.__name__), endTime - startTime)
        )

    def _stripSuffix(self, fileName):
        return re.sub("(^.*)\\.py", "\\1", fileName)

    def _allTestClasses(self, module):
        return [
            module.__dict__[name]
            for name in module.__dict__.keys()
            if self._isTestClassName(name)
        ]

        result = []
        for name in module.__dict__.keys():
            if self._isTestClassName(name):
                result.append(module.__dict__[name])

        return result

    def _isTestClassName(self, name):
        return re.search("^ut_", name)

    def _allTestFuncs(self, testClass):
        result = []
        for name in testClass.__dict__.keys():
            if self._isTestFuncName(name):
                func = testClass.__dict__[name]
                if callable(func):
                    result.append(func)

        return result

    def _isTestFuncName(self, name):
        return re.search("^test", name)

    def _printStackTrace(self, tb):
        frames = [
            self._fixFrame(frame)
            for frame in extract_tb(tb)
            if os.path.basename(frame[0]) != "teest.py"
        ]
        trace = format_list(frames)
        sys.stdout.write("".join(trace))

    def _fixFrame(self, frame):
        result = [item for item in frame]
        if os.path.dirname(result[0]) == self.homeDir:
            result[0] = os.path.basename(result[0])
        return result

    def _numTestsRun(self):
        return "(%d %s run)" % (self.numTests, self._testWord(self.numTests))

    def _testWord(self, num):
        if num == 1:
            return "test"
        else:
            return "tests"

    def _exceptionMsg(self, exc):
        result = exc.__class__.__name__
        s = str(exc).strip()
        if len(s) > 0:
            result += ": " + str(exc)

        return result


def switchInFirstArgv():
    global showTimings, timingsLimit

    try:
        switch = sys.argv[1]
    except IndexError:
        return False

    if switch.startswith("-"):
        m = re.match("(-t)(\d+)", switch)
        if m:
            showTimings = TestRunner.timingsByTime
            timingsLimit = int(m.groups()[1])
        else:
            if switch == "-t":
                showTimings = TestRunner.timingsByTime
            elif switch == "-n":
                showTimings = TestRunner.timingsByName

        del sys.argv[1]
        return True
    else:
        return False


utPattern = re.compile("^ut.*\.py$")


def allUts():
    return [filename for filename in os.listdir(".") if utPattern.match(filename)]


if __name__ == "__main__":
    while switchInFirstArgv():
        pass

    if len(sys.argv) > 1:
        runner = TestRunner(sys.argv[1:])
    else:
        runner = TestRunner(allUts())

    if showTimings:
        print(showTimings(runner))
    sys.exit(runner.numFailedTests != 0)
