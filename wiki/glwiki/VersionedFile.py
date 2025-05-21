import re, time

from WikiRepository import PageFile

ST_NOT_IN_VERSION = 0
ST_IN_VERSION = 1


class BadVersionException(Exception):

    def __init__(self, versionNum=None):
        self.versionNum = versionNum

    def __str__(self):
        return "non-existent wiki-page version: %s" % str(self.versionNum)


class VersionInfo:

    def __init__(self, versionNumOrLine, date=None, author=None):
        # if only one argument, then we've been passed a line from a VersionedFile
        if date == None:
            line = versionNumOrLine
            dict = _parse(line)
            if "version" in dict:
                for key in dict.keys():
                    self.__dict__[key] = dict[key]
        else:
            self.version = versionNumOrLine
            self.date = date
            self.author = author

    def text(self):
        return "@@ version %d; date %s; author %s;\n" % (
            int(self.version),
            str(self.date),
            str(self.author),
        )


class VersionedFile:

    def __init__(self, rawFileOrPageFile):
        if rawFileOrPageFile.__class__ == PageFile:
            self.rawFile = rawFileOrPageFile.openForReading()
            self.pageFile = rawFileOrPageFile
        else:
            self.rawFile = rawFileOrPageFile

    def numVersions(self):
        count = 0
        self.rawFile.seek(0)

        for line in self.rawFile:
            if line.startswith("@@"):
                line = line[2:].strip()
                if re.match("^version\s", line):
                    count += 1

        return count

    def getVersion(self, versionNum):
        result = []
        self.rawFile.seek(0)
        state = ST_NOT_IN_VERSION
        fileHasVersioning = False
        foundVersion = False

        for line in self.rawFile:
            if state == ST_NOT_IN_VERSION:
                if line.startswith("@@"):
                    line = line[2:].strip()
                    fileHasVersioning = True
                    if (
                        re.match("^hereis\s", line)
                        and _versionNumFromHereis(line) == versionNum
                    ):
                        state = ST_IN_VERSION

            else:
                assert state == ST_IN_VERSION
                if line.startswith("@@"):
                    break

                result.append(line)
                foundVersion = True

        if fileHasVersioning:
            if not foundVersion:
                raise BadVersionException(versionNum)
        else:
            # if no versioning, just return the whole file
            if state == ST_NOT_IN_VERSION:
                self.rawFile.seek(0)
                result = self.rawFile.readlines()

        return result

    def getLatestVersion(self):
        return self.getVersion(self.maxVersionNum())

    def getLatestAuthor(self):
        return self.getVersionList()[-1].author

    def getVersionList(self):
        result = []
        self.rawFile.seek(0)

        for line in self.rawFile:
            if line.startswith("@@"):
                if re.match("@@\s*version\s", line):
                    result.append(VersionInfo(line))

        return result

    def getVersionInfo(self, versionNum):
        list = self.getVersionList()
        if len(list) == 0:
            return VersionInfo(0, "0.0.0.0.0.0", "(unknown)")

        for item in list:
            if str(item.version) == str(versionNum):
                return item

        raise BadVersionException(versionNum)

    def getLatestVersionNum(self):
        try:
            return max([int(item.version) for item in self.getVersionList()])
        except ValueError:
            return 1

    def writeNewVersion(self, command):  # TODO delete
        self.writeNewVersion2(command.userName, command.inputFile)

    def writeNewVersion2(self, userName, inputFile):
        versions = self.getVersionList()
        # versions.sort(lambda a, b: cmp(int(b.version), int(a.version)))
        versions.sort(key=lambda x: int(x.version), reverse=True)
        if len(versions) == 0:
            versionNum = 1
        else:
            versionNum = int(versions[0].version) + 1
        newVersion = VersionInfo(str(versionNum), _dateString(), userName)

        # read all the old versions in

        versionTexts = {}
        for version in versions:
            v = int(version.version)
            versionTexts[v] = self.getVersion(v)  # TODO: awfully inefficient

        # write VersionInfo lines

        self.rawFile.seek(0)
        self.rawFile.truncate()

        self.rawFile.write(newVersion.text())
        for version in versions:
            self.rawFile.write(version.text())

        # write the text of all the versions

        # print >> self.rawFile, "@@ hereis %d" % versionNum
        self.rawFile.write("@@ hereis %d\n" % versionNum)
        self.rawFile.write(_readAllText(inputFile))

        for version in versions:
            v = int(version.version)
            # print >> self.rawFile, "@@ hereis %d" % v
            self.rawFile.write("@@ hereis %d\n" % v)
            self.rawFile.write("".join(versionTexts[v]))

    def maxVersionNum(self):
        if _fileSize(self.rawFile) == 0:
            return 0

        versionList = self.getVersionList()
        if len(versionList) == 0:
            return 1
        else:
            return max([int(v.version) for v in versionList])

    def getLatestVersionInfo(self):
        result = None
        versionList = self.getVersionList()
        for version in versionList:
            if result == None or int(version.version) > int(result.version):
                result = version

        if result == None:
            return VersionInfo(
                "0", _makeDateString(self.pageFile.getModificationTime()), "(unknown)"
            )
        else:
            return result

    def close(self):
        self.rawFile.close()


def _versionNumFromHereis(strippedLine):
    words = re.split("\W+", strippedLine)
    if len(words) >= 2:
        return int(words[1])
    else:
        return 0


def _dateString():
    return ".".join([str(n) for n in time.gmtime()[:6]])


def _makeDateString(tup):
    return ".".join([str(n) for n in tup[:6]])


def _parse(line):
    result = {}

    if not line.startswith("@@"):
        return result

    line = line[2:].strip()

    for nameValuePair in re.split(";\s*", line):
        words = re.split("\s+", nameValuePair, 1)
        if len(words) == 2:
            result[words[0]] = words[1]

    return result


def _readAllText(f):
    result = "".join(f)
    if not result.endswith("\n"):
        result += "\n"

    return result


def _fileSize(f):
    f.seek(0, 2)
    return f.tell()
