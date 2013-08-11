import re
from symbol import Sym, quotes
from collections import Namedtuple

AstNode = Namedtuple(["tok", "line", "start", "end", "exp"])


class AstNode(object):

    def __init__(self, tok, line, start, end):
        self.tok, self.line, self.start, self.end = tok, line, start, end
        self.exp = None

    def throwaway(self):
        return self.tok is None or re.match("^\s+$", self.tok)

    def __repr__(self):
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
    return map(lambda t: (t, line, _str.index(t), _str.index(t) + len(t)), tokens)

def tokenize(_str):
    splitter = re.compile("""(\s+|\(|\)|"|[^\s"\(\),@'`#\[\]\}\{]+|[,`'@#]{1,3}|[\[\]\{\}])""")
    return getpos(filter(lambda s: s != "" and s is not None, splitter.split(_str)), _str)


def read_string(node, tokens):
    L = []
    while tokens[0][0] != "\"":
        t, _, _, end = tokens.pop(0)
        L.append(t)
    node.end = tokens.pop(0)[3]
    node.exp = "".join(L)
    node.tok = "\"%s\"" % node.exp


def read_sexp(node, tokens):
    node.exp = []
    while tokens[0][0] != ")":
        node.exp.append(read(tokens))
    tokens.pop(0)
    node.end = node.exp[-1].end
    node.tok = "(%s)" % " ".join([n.tok for n in node.exp])


def read_quoted(node, tokens):
    node.exp = (quotes[node.tok], read(tokens))
    node.tok += node.exp[1].tok
    node.end = node.exp[1].end

def read(tokens):
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    node = AstNode(*tokens.pop(0))
    if node.throwaway():
        return read(tokens)
    else:
        if node.tok in quotes:
            read_quoted(node, tokens)
        elif "\"" == node.tok:
            read_string(node, tokens)
        if "(" == node.tok:
            read_sexp(node, tokens)
        elif ")" == node.tok:
            raise SyntaxError("Unexpected )")
        else:
            node.exp = atom(node.tok)
        return node


def parse(_str):
    tokens = tokenize(_str)
    while tokens:
        yield read(tokens)


if  __name__ == "__main__":
    print read(tokenize("(define (hello who) (print `hello who))"))
