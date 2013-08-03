from parsing import parse
from analysis import analyze
from environment import make_global_env
import sys

def repl():
    env = make_global_env()
    def ask():
        try:
            _str = raw_input("=> ")
        except KeyboardInterrupt:
            print "bye"
            sys.exit(0)
        try:
            val = analyze(parse(_str))(env)
        except Exception as e:
            val = "%s: %s" % (type(e).__name__, str(e))
        print val
        ask()
    ask()

if __name__ == "__main__":
    print "=============\nlois.py v.0.0.1\n============="
    repl()