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
    tokens = "(" + "|".join(["\s+", "\(", "\)", "\"", "[^\s\"\(\),@'`]+", "'", "`", ",(!?@)", ",@"]) + ")"
    splitter = re.compile(tokens)
    return filter(lambda s: s != "" and s is not None, splitter.split(_str))

_quote, _quasiquote, _unquote, _unquotesplicing = Sym("quote"), Sym("quasiquote"), Sym("unquote"), Sym("unquote-splicing")

quotes = {
    "`": _quote,
    "'": _quasiquote,
    ",": _unquote,
    ",@": _unquotesplicing}

def read(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    t = tokens.pop(0) # get first token
    if t is None or re.match("^\s+$", t): # throw away whitespace if not in a string
        return read(tokens)
    elif t in quotes: # return quoted list|symbol as tagged list.
        print tokens
        return [quotes[t], read(tokens)]
    elif "\"" == t: # string
        L = []
        while tokens[0] != "\"":
            L.append(tokens.pop(0))
        tokens.pop(0)
        return "".join(L)
    if "(" == t: # sexp
        L = []
        while tokens[0] != ")":
            L.append(read(tokens))
        tokens.pop(0)
        return L
    elif ")" == t:
        raise SyntaxError("Unexpected )")
    else:
        return atom(t) # literal


def parse(_str):
    tokens = tokenize(_str)
    while tokens:
        yield read(tokens)
