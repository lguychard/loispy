from error import Error


class CodeObject(object):

    def __init__(self, astnode, code):
        self.node, self.code = astnode, code

    def exec_(self, env):
        """ Run the analyzed code in the context of an environment """
        val = self.code(env)
        if type(val) == Error and val.codeobj is None:
            val.codeobj = self
        return val
