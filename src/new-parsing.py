from parsing import Sym

original_str = "(+ 1 2)"

parsed_tree1 = {
    "str": "(+ 1 2)", # Original string, before parsing
    "loc": (1, 0, 6), # Location of string in program: line number, start index, end index
    "exp": [
        {
            "str": "+",
            "loc": (1, 1, 1),
            "exp": Sym("+")
        }, {
            "str": "1",
            "loc": (1, 3, 3),
            "exp": 1
        }, {
            "str": "2",
            "loc": (1, 6, 6),
            "exp": 2
        }
    ]
}

parsed_tree2 = ("tok", "(+ 1 2)", (1, 0, 6), (
    ("tok", "+", (1, 1, 1), Sym("+")),
    ("tok", "1", (1, 3, 3), 1),
    ("tok", "2", (1, 6, 6), 2)
    ))

def is_tok(exp):
    return exp[0] == "tok"

def tok_str(tok):
    return tok[1]

def tok_loc(tok):
    return tok[2]

def tok_exp(tok):
    return tok[3]

def format_lok(tok_loc):
    return "line %d, char%d-%d" % (tok_loc[0], tok_loc[1], tok_loc[2])

