from procedure import Procedure

class Inspector(Procedure):
    """ provides access to its enclosing environment """
    def __call__(self):
        return self.env.__repr__()

def inspect():
    return lambda env: Inspector([], None, env)

