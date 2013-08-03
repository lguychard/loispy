import re

class Symbol(str):

    def __str__(self):
        return "Sym(%s)" % super(Symbol, self).__str__()

    def __repr__(self):
        return __str__(self)

def Sym(s, symbol_table={}):
    symbol_table[s] = Symbol(s)
    return symbol_table[s]

def atom(tok):
    booleans = {"#t":True, "#f":False, "#n":None}
    if tok in booleans:
        return booleans[tok]
    elif re.match("^\d+$", tok):
        return int(tok)
    elif re.match("^\d+\.\d+$", tok):
        return float(tok)
    else:
        return Sym(tok)

def tokenize(_str):
    _str = _str.replace("(", " ( ").replace(")", " ) ")
    return _str.split()

def read(tokens):
    print tokens
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    t = tokens.pop()
    if "(" == t:
        L = []
        while tokens[0] != ")":
            L.append(read(tokens))
        tokens.pop()
        return L
    elif ")" ==t:
        raise SyntaxError("Unexpected )")
    else:
        return atom(t)

def parse(_str):
    return read(tokenize(_str))