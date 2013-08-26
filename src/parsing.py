import re
from symbol import Symbol, Sym, quotes, _dict
from utils import isa


class AstNode(object):
    """
    Represents a node in the loispy AST.
    """
    def __init__(self, tok, line, start, end):
        self.tok, self.line, self.start, self.end = tok, line, start, end
        self.exp = None

    def throwaway(self):
        return self.tok is None or re.match("^\s+$", self.tok)

    def get_exp(self):
        if isa(self.exp, list):
            if self.exp[0] is _dict:
                return dict(zip(*[n.get_exp() for l in self.exp[1:] for n in l]))
            else:
                return [n.get_exp() for n in self.exp]
        else:
            return self.exp

    def __str__(self):
        return "<AstNode '%s' at %d:%d,%d>%s\n" % \
                    (self.tok, self.line, self.start, self.end, self.exp)


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
    # Obviously this doesn't work. But i'll figure it out later.
    # The general idea is to attach positional info to each tokens.
    return map(lambda t: (t, line, _str.index(t), _str.index(t) + len(t)), tokens)


def split(_str):
    return re.compile("(" + "|".join([
        "\s+",                          # whitespace
        "#t", "#f", "#n",               # booleans
        "\(", "\)",                     # parens
        """[^\s"\(\),@'`#\[\]\}\{]+""", # symbols
        "'", "`", ",@?", "#",           # quotes, lambda shorthand
        "[\[\]\{\}]"                    # square and curly brackets
        ]) + ")").split(_str)


def not_useless(tok):
    return tok != "" and tok is not None


def tokenize(_str):
    _str = re.sub(";.*\n", "", _str)
    _str = re.sub("\s+$", "", _str)
    return getpos(filter(not_useless, split(_str)), _str)


def read_string(node, tokens):
    """
    Accumulate tokens until a double-quote is found, without throwing away
    whitespace. Set the 'exp' property of the node argument to the accumulated
    tokens joined as a string. Pop off the closing double quote. Return the
    mutated node.

    @param AstNode node
    @param list tokens

    @returns AstNode
    """
    L = []
    while tokens[0][0] != "\"":
        t, _, _, end = tokens.pop(0)
        L.append(t)
    node.end = tokens.pop(0)[3]
    node.exp = "".join(L)
    node.tok = "\"%s\"" % node.exp
    return node


def read_list(node, tokens):
    node.exp = []
    while tokens[0][0] != ")":
        node.exp.append(read(tokens))
    tokens.pop(0)
    if node.exp:
        node.end = node.exp[-1].end
    else:
        node.end += 1
    node.tok = "(%s)" % " ".join([n.tok for n in node.exp])
    return node


def read_quoted(node, tokens):
    node.exp = quotes[node.tok]
    exp = [node, read(tokens)]
    tok = node.tok + exp[1].tok
    line, start, end = node.line, node.start, exp[1].end
    quotednode = AstNode(tok, line, start, end)
    quotednode.exp = exp
    return quotednode


def read_key(tokens):
    node = read(tokens)
    if not isa(node.exp, Symbol)  or node.tok[0] != ":":
        raise SyntaxError("Key formatting error: %s" % node.tok)
    node.exp = Sym(node.exp[1:])
    return node


def read_dict(node, tokens):
    node.exp = [_dict, [], []]
    while tokens[0][0] != "}":
        node.exp[1].append(read_key(tokens))
        node.exp[2].append(read(tokens))
    tokens.pop(0)
    return node


def read(tokens):
    """
    Iterates through a list of strings (tokens) and returns an AstNode object.
    Warning: this function has side-effects: it mutates its argument (tokens)

    @param list[str] tokens

    @returns AstNode
    """
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    node = AstNode(*tokens.pop(0))
    if node.throwaway():
        return read(tokens)
    else:
        if node.tok in quotes:
            return read_quoted(node, tokens)
        elif "\"" == node.tok:
            return read_string(node, tokens)
        elif "(" == node.tok:
            return read_list(node, tokens)
        elif "{" == node.tok:
            return read_dict(node, tokens)
        elif node.tok in ["}", ")", "]", "["]:
            raise SyntaxError("Unexpected token: %s in %s" %
                                            (node.tok, [t[0] for t in tokens]))
        else:
            node.exp = atom(node.tok)
            return node


def parse(_str):
    """
    Parses all the expressions in a given string
    and provide them as a generator.

    @param str _str

    @yields AstNode
    """
    tokens = tokenize(_str)
    while tokens:
        yield read(tokens)
