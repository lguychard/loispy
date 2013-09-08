class CodeObject(object):

    def __init__(self, astnode, code):
        self.node, self.code = astnode, code

    def exec_(self, env):
        """ Run the analyzed code in the context of an environment """
        try:
            val = self.code(env)
            return val
        except Exception as e:
            raise NotImplementedError
