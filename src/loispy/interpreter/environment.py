from builtin import builtin


class Environment(dict):
    """
    'An environment is a sequence of frames. Each frame is a table (possibly
    empty) of bindings, which associate variable names with their corresponding
    values. (A single frame may contain at most one binding for any variable.)
    Each frame also has a pointer to its enclosing environment, unless, for the
    purposes of discussion, the frame is considered to be global.'
    [ABELSON et al., 1996]
    """

    def __init__(self, _vars={}, outer=None):
        self.update(_vars)
        # pointer to the enclosing environment
        self.outer = outer

    def find(self, var):
        """
        'The value of a variable with respect to an environment is the value
        given by the binding of the variable in the first frame in the
        environment that contains a binding for that variable. If no frame in
        the sequence specifies a binding for the variable, then the variable
        is said to be unbound in the environment.'
        [ABELSON et al., 1996]
        """
        if var in self:
            return self
        elif not self.outer:
            raise NameError("%s unbound in current scope" % var)
        else:
            return self.outer.find(var)

    def set(self, var, val):
        self[var] = val


# 'To describe interactions with the interpreter, we will suppose that there
# is a global environment, consisting of a single frame (with no enclosing
# environment) that includes values for the symbols associated with the
# primitive procedures. For example, the idea that + is the symbol for
# addition is captured by saying that the symbol + is bound in the global
# environment to the primitive addition procedure.'
# [ABELSON et al., 1996]

THE_GLOBAL_ENV = Environment(builtin)
