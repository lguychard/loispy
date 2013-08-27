from environment import Environment


class Procedure(object):
    """
    Represents a loisp procedure. A procedure encapsulates a body (sequence of
    instructions) and a list of arguments. A procedure may be called: the body
    of the procedure is evaluated in the context of an environment, and given

    """

    def __init__(self, env, args, body, name=""):
        """
        @param Environment env
        @param list[str] args
        @param function body
        @param str name
        """
        self.env = env
        self.args = args
        # Check now if the procedure has variable arguments
        self.numargs = -1 if len(args) >= 1 and "..." in args[-1] else len(self.args)
        if self.numargs == -1:
            self.numpositional = len(self.args) -1
            self.positional = self.args[:self.numpositional]
            self.vararg = self.args[-1].replace("...", "")
        self.body = body
        self.name = name

    def __call__(self, *argvals):
        """
        'the procedure body for a compound procedure has already been analyzed,
        so there is no need to do further analysis. Instead, we just call
        the execution procedure for the body on the extended environment.'
        [ABELSON et al., 1996]
        """
        call_env = Environment(self.pack_args(argvals), self.env)
        return self.body.__call__(call_env)

    def pack_args(self, argvals):
        """
        Return a dict mapping argument names to argument values at call time.
        """
        if self.numargs == -1:
            if len(argvals) <= self.numpositional:
                raise Exception("Wrong number of arguments for '%s' (%d)" %
                    (self.name, len(argvals)))
            _vars = dict(zip(self.positional, argvals[:self.numpositional]))
            _vars.update({self.vararg : argvals[self.numpositional:]})
        else:
            if len(argvals) != self.numargs:
                raise Exception("Wrong number of arguments for '%s' (%d)" %
                    (self.name, len(argvals)))
            _vars = dict(zip(self.args, argvals))
        return _vars

    def __str__(self):
        return "<Procedure %s>" % self.name if self.name else "<Procedure>"

    def __repr__(self):
        return self.__str__()

