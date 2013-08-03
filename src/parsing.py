import re

class Symbol(str):
    def __str__(self):
        return super(Symbol, self).__str__()
    def __repr__(self):
        return self.__str__()

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

# TODO: rewrite read & tokenize so that they're not shit

def tokenize(_str):
    _str = _str.replace("(", " ( ").replace(")", " ) ").replace("\"", " \" ")
    return _str.split()

def read(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    t = tokens.pop(0)
    if "\"" == t:
        L = []
        while tokens[0] != "\"":
            L.append(tokens.pop(0))
        tokens.pop(0)
        return " ".join(L)
    if "(" == t:
        L = []
        while tokens[0] != ")":
            L.append(read(tokens))
        tokens.pop(0)
        return L
    elif ")" == t:
        raise SyntaxError("Unexpected )")
    else:
        return atom(t)

def parse(_str):
    return read(tokenize(_str))