import time

from Misc import stripLeadingSlash


def log(environ, commandName, uri, userName):
    logFile = open("wikilog", "a")

    logFile.write(
        "%s  %-15s %-6s %s %s\n"
        % (
            time.strftime("%a %d-%b-%Y %H:%M:%S"),
            _userNameWithIP(userName, environ.get("REMOTE_ADDR", "-")),
            commandName,
            stripLeadingSlash(_dashIfBlank(uri)),
            environ.get("HTTP_REFERER", "-"),
        )
    )

    logFile.close()


def _dashIfBlank(s):
    if len(s) == 0:
        return "-"
    else:
        return s


def _userNameWithIP(userName, ip):
    if userName and userName != "(unknown)" and userName != ip:
        return "%s(%s)" % (userName, ip)
    else:
        return ip
