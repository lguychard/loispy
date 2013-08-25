

class Error(object):

    def __init__(self, codeobj=None, msg=None, exc=None):
        self.codeobj = codeobj
        self.stack = []
        self.msg = msg if msg else "%s" % exc if exc else ""

    def __repr__(self):
        self.at = "    at %d:%d,%d: '%s'" % (
            self.codeobj.node.line,
            self.codeobj.node.start,
            self.codeobj.node.end,
            self.codeobj.node.tok)
        return "\n".join(["<Error: %s>" % self.msg, self.at] +
                         ["    at %s" % name for name in self.stack[:6]])

    def __str__(self):
        return self.__repr__()


def error(msg=""):
    return Error(msg=msg)