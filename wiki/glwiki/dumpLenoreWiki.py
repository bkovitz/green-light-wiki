from VersionedFile2 import VersionedFile2
from WikiRepository import WikiRepository

def printAllVersions(f):
    pageFile = repo.pageFile(pageName)
    f = pageFile.openForReading()
    v = VersionedFile2(f)

    for i in range(1, v.getLatestVersionNum() + 1):
        print('page name:', pageName)
        info = v.getVersionInfo(i)
        print('versionNum:', info.versionNum)
        print('date:', info.date)
        print('author:', info.author)
        print('text:', )
        for line in v.getVersion(i):
            print(line, end='')
        print("@@")


repo = WikiRepository('../lenore-exegesis')

for pageName in repo.allPageNames():
    printAllVersions(pageName)
