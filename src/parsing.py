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


def getpos(tokens, _str, line=1):
    return map(lambda t: (t, line, _str.index(t), _str.index(t) + len(t)), tokens)

def tokenize(_str):
    tokens = "(" + "|".join(["\s+", "\(", "\)", "\"", "[^\s\"\(\),@'`\[\]\{\}]+", "[`',@]{1,3}"]) + ")"
    splitter = re.compile(tokens)
    return getpos(filter(lambda s: s != "" and s is not None, splitter.split(_str)), _str)

_quote, _quasiquote, _unquote, _unquotesplicing = Sym("quote"), Sym("quasiquote"), Sym("unquote"), Sym("unquote-splicing")

quotes = {
    "`": _quote,
    "'": _quasiquote,
    ",": _unquote,
    ",@": _unquotesplicing}

def read(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    tok, line, start, end = tokens.pop(0) # get first token
    if tok is None or re.match("^\s+$", tok): # throw away whitespace if not in a string
        return read(tokens)
    elif tok in quotes: # return quoted list|symbol as tagged list.
        return ([quotes[t], read(tokens)])
    elif "\"" == tok: # string
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


if  __name__ == "__main__":
    print tokenize("(define (hello who) (print \"Hello\" who))")