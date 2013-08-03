from parsing import parse
from analysis import _exec
from environment import make_global_env
import debug
import sys
import traceback
from utils import to_string

def repl(dbg=True):
    env = make_global_env()
    if dbg:
        env.update(vars(debug))
    def ask():
        try:
            _str = raw_input("=> ")
        except KeyboardInterrupt:
            print "bye"
            sys.exit(0)
        try:
            val = _exec(parse(_str), env)
        except Exception as e:
            val = "%s: %s" % (type(e).__name__, str(e))
            print traceback.format_exc()
        if val is not None:
            print to_string(val)
    print "===============\nlois.py v.0.0.1\n==============="
    while True:
        ask()

def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as _file:
            print _exec(parse(_file.read()), make_global_env())
    elif len(sys.argv) == 1:
        repl()
    else:
        raise Exception("Too many arguments")

if __name__ == "__main__":
    main()