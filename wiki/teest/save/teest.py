import sys, re, exceptions, string
import imp, inspect

numFailedTests = 0


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


def main():
    for fileName in sys.argv[1:]:
        runTests(fileName)

    if numFailedTests == 0:
        print("All tests PASSED.")
        return 0
    else:
        if numFailedTests == 1:
            print("1 test FAILED.")
        else:
            print(numFailedTests, "tests FAILED.")
        return 1


def runTests(fileName):
    global numFailedTests

    moduleName = stripSuffix(fileName)
    file, path, description = imp.find_module(moduleName)
    module = imp.load_source(moduleName, path, file)

    for testClass in testClasses(module):
        for testFunc in testFuncs(testClass):
            obj = testClass()

            try:
                testFunc(obj)
            except Exception as exc:
                print("%s.%s FAILED" % (testClass.__name__, testFunc.__name__))
                printStackTrace(inspect.trace())
                print("    " + str(exc))
                numFailedTests += 1


def stripSuffix(fileName):
    return re.sub("(^.*)\\.py", "\\1", fileName)


def testClasses(module):
    result = []
    for name in module.__dict__.keys():
        if isTestClassName(name):
            result.append(module.__dict__[name])

    return result


def isTestClassName(name):
    return re.search("^ut_", name)


def testFuncs(testClass):
    result = []
    for name in testClass.__dict__.keys():
        if isTestFuncName(name):
            func = testClass.__dict__[name]
            if callable(func):
                result.append(func)

    return result


def isTestFuncName(name):
    return re.search("^test", name)


def printStackTrace(frames):
    for frame in frames[1:-1]:
        printStackFrame(frame)


def printStackFrame(frame):
    fr, fileName, lineNum, function, lines, index = frame
    print("%s:%d in function %s:" % (fileName, lineNum, function))
    line = str(lines[index]).lstrip()
    print("    %s" % line[:-1])


if __name__ == "__main__":
    sys.exit(main())
