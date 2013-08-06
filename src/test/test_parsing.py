import sys
sys.path.append("./../")
from parsing import parse, Sym, _unquote, _quote

tests = [
    # Basic datatypes
    ("1", 1),
    ("0.24", 0.24),
    ("\"Hello world!\"", "Hello world!"),
    ("#t", True),
    ("#f", False),
    ("#n", None),
    ("define", Sym("define")),
    # simple expressions
    ("(+ 1 2)", [Sym("+"), 1, 2]),
    ("`hello", [_quote, Sym("hello")]),
    (",(1 2 3)", [_unquote, [1, 2, 3]]),
    ("(define (add a b) (+ a b))", [Sym("define"),
                                    [Sym("add"), Sym("a"), Sym("b")],
                                    [Sym("+"), Sym("a"), Sym("b")]]),
    ("(define (say what) (print \"says:\" what))", [Sym("define"),
                                                        [Sym("say"), Sym("what")],
                                                        [Sym("print"), "says:", Sym("what")]])
]

def run_tests():
    failed = 0
    for t in tests:
        # try:
        out = parse(t[0]).next()
        # except Exception, e:
        #     out = "%s: %s" % (type(e).__name__, str(e))
        res = "SUCCESS" if t[1] == out else "FAIL"
        if res == "FAIL":
            failed += 1
        print t[0], " => ", out.__repr__(), " --- ", res
    print "\n-------------------------\n"
    print "ran %d tests, %d failed, %d successful" % (
            len(tests), failed, len(tests) - failed)

if __name__ == "__main__":
    run_tests()