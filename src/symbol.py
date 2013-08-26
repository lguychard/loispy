# ------------
# SYMBOL CLASS
# ------------


class Symbol(str):
    """
    'Now that we have strings, Symbols will be implemented
    as a separate class, which derives from str' [NORVIG 2010]
    """
    pass


def Sym(s, symbol_table={}):
    """
    'Manages a symbol table of unique symbols' [NORVIG 2010]
    """
    symbol_table[s] = Symbol(s)
    return symbol_table[s]


# -----------------
# LANGUAGE KEYWORDS
# -----------------


_if = Sym("if")
_begin = Sym("begin")
_vardef = Sym("$")
_procdef = Sym("=>")
_macrodef = Sym("macro=>")
_lambdashorthand = Sym("#")
_let = Sym("let")
_lambda = Sym("lambda")
_set = Sym("set!")
_else = Sym("else")
_dict = Sym("$dict$")
_key = Sym("$key$")

# ------
# QUOTES
# ------

_quote = Sym("quote")
_quasiquote = Sym("quasiquote")
_unquote = Sym("unquote")
_unquotesplicing = Sym("unquote-splicing")

quotes = {
    "'": _quote,
    "`": _quasiquote,
    ",": _unquote,
    ",@": _unquotesplicing,
    "#": _lambdashorthand
    }
