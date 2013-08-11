

class Symbol(str):
    def __str__(self):
        return super(Symbol, self).__str__()
    def __repr__(self):
        return self.__str__()


def Sym(s, symbol_table={}):
    symbol_table[s] = Symbol(s)
    return symbol_table[s]

#
# LANGUAGE KEYWORDS
#

# quotes

_quote = Sym("quote")
_quasiquote = Sym("quasiquote")
_unquote = Sym("unquote")
_unquotesplicing = Sym("unquote-splicing")


quotes = {
    "`": _quote,
    "'": _quasiquote,
    ",": _unquote,
    ",@": _unquotesplicing,
    "quote": _quote,
    "quasiquote": _quasiquote,
    "unquote": _unquote,
    "unquote-splicing": _unquotesplicing
    }

# keywords

_if, _define, _begin, _let, _defmacro, _cond = Sym("if"), Sym("define"), Sym("begin"), Sym("let"), Sym("define-macro"), Sym("cond")