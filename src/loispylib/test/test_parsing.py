import sys
sys.path.append("./../..")
from loispylib.parsing import parse, Sym

tests = [
    # Basic datatypes
    ("1", 1),
    ("0.24", 0.24),
    ("#t", True),
    ("#f", False),
    ("#n", None),
    ("define", Sym("define")),
    # simple expressions
    ("(+ 1 2)", [Sym("+"), 1, 2]),
    ("(define (add a b) (+ a b))", [Sym("define"),
                                    [Sym("add"), Sym("a"), Sym("b")],
                                    [Sym("+"), Sym("a"), Sym("b")]])
]

def run_tests():
    failed = 0
    for t in tests:
        try:
            out = parse(t[0])
        except Exception, e:
            out = "%s: %s" % (type(e).__name__, str(e))
        res = "SUCCESS" if t[1] == out else "FAIL"
        if res == "FAIL":
            failed += 1
        print t[0], " => ", out, " --- ", res
    print "\n-------------------------\n"
    print "ran %d tests, %d failed" % (len(tests), failed)

if __name__ == "__main__":
    run_tests()