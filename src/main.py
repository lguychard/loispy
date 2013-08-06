from parsing import parse
from analysis import analyze, _eval
from environment import make_global_env
import sys
import traceback
from utils import to_string
from argparse import ArgumentParser
from collections import Counter


def repl(env, debug=False):
    # TODO: multiline, nicer REPL. Tab-completion
    def ask():
        try:
            _str = raw_input("=> ")
            matched = paren_match(_str)
            while not matched:
                _str += raw_input(".. ")
                matched = paren_match(_str)
        except KeyboardInterrupt:
            print "bye"
            sys.exit(0)
        try:
            val = _eval(_str, env)
            if len(val) != 1:
                raise Exception("Expected 1 return value, got %d" % len(val))
            val = val.pop()
        except Exception as e:
            val = e
            if debug:
                print traceback.format_exc()
        if val is not None:
            print to_string(val)
    print "===============\nlois.py v.0.0.1\n==============="
    while True:
        ask()


def paren_match(_str):
    c = Counter(_str)
    return c["("] == c[")"] and c["\""] % 2 == 0


def run(filename, env):
    with open(filename, "r") as _file:
        for exp in parse(_file.read()):
            val = analyze(exp)(env)
            if val is not None:
                print val

def load(filename, env):
    with open(filename, "r") as _file:
        for exp in parse(_file.read()):
            analyze(exp)(env)


def make_argparser():
    parser = ArgumentParser(description="loispy interpreter")
    parser.add_argument("file", nargs="?", default=None,
        help="A file to run directly")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug flag")
    parser.add_argument("-l", "--load", nargs="*", default=[],
        help="A list of files to eval before doing anything else.")
    return parser


def main():
    args = make_argparser().parse_args()
    env = make_global_env()
    for f in args.load:
        load(f, env)
    if not args.file:
        repl(env)
    else:
        print run(args.file, env)


if __name__ == "__main__":
    main()
