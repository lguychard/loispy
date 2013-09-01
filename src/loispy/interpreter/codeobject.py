from error import Error


class CodeObject(object):

    def __init__(self, astnode, code):
        self.node, self.code = astnode, code

    def exec_(self, env):
        """ Run the analyzed code in the context of an environment """
        try:
            val = self.code(env)
            return val
        except Error as e:
            if e.codeobj is None:
                e.codeobj = self
                raise e
        except Exception as e:
            raise Error(codeobj=self, exc=e)
