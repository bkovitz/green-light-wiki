import os

from File import PipeFrom
from Config import config


class PipeFromPhp(PipeFrom):

    def __init__(self, phpFile):
        self.filename = "php"
        self._env = _makeEnv()
        self._args = [
            _makeFullPathToPhpFile(phpFile),
            os.environ.get("QUERY_STRING", ""),
        ]

        self._open()


def _makeEnv():
    result = {}

    for var in ["PATH", "PWD", "REMOTE_ADDR", "HTTP_COOKIE"]:
        try:
            result[var] = os.environ[var]
        except KeyError:
            pass

    return result


def _makeFullPathToPhpFile(phpFile):
    baseDir = config.get("", "base directory")

    if not baseDir:
        return phpFile
    else:
        return baseDir + "/" + phpFile
