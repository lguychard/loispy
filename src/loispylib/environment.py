
class Environment(dict):

    def __init__(self, _vars={}, outer=None):
        self.update(_vars)
        self.outer = outer

    def find(self, var):
        if var in self:
            return self
        elif not outer:
            raise NameError("%s undefined in current scope" % var)


def make_global_env():
    ret