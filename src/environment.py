from native import native

class Environment(dict):

    def __init__(self, _vars={}, outer=None):
        self.update(_vars)
        self.outer = outer

    def find(self, var):
        if var in self:
            return self
        elif not self.outer:
            raise NameError("%s undefined in current scope" % var)
        else:
            return self.outer.find(var)

    def set(self, var, val):
        self[var] = val


def make_global_env():
    return Environment(native)

