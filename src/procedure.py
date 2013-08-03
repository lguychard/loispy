from environment import Environment


class Procedure(object):

    __slots__ = ["env", "args", "body", "numargs", "name"]

    def __init__(self, env, args, body, name="lambda"):
        self.env = env
        self.args = args
        self.body = body
        self.numargs = len(self.args)
        self.name = name

    def __call__(self, *argvals):
        if len(argvals) != self.numargs:
            raise TypeError("Wrong number of arguments: %d" % len(argvals))
        _vars = dict(zip(self.args, argvals))
        call_env = Environment(_vars, self.env)
        return self.body.__call__(call_env)

    def __str__(self):
        return "<Procedure %s>" % self.name

    def __repr__(self):
        return self.__str__()
