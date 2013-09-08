from analysis import eval
from environment import THE_GLOBAL_ENV
import sys
import traceback
from utils import to_string
from argparse import ArgumentParser
from collections import Counter


def repl(env=THE_GLOBAL_ENV, debug=False):
    # TODO: nicer REPL. Tab-completion
    def ask():
        try:
            _str = raw_input("=> ")
            if not _str:
                ask()
            else:
                matched = paren_match(_str)
                while not matched:
                    _str += raw_input(".. ")
                    matched = paren_match(_str)
        except KeyboardInterrupt:
            print "bye"
            sys.exit(0)
        try:
            val = eval(_str, env)
        except Exception as e:
            val = e
            # if debug:
            #     print traceback.format_exc()
        print to_string(val)
    print "===============\nlois.py v.0.0.1\n==============="
    while True:
        ask()


def paren_match(_str):
    c = Counter(_str)
    return c["("] == c[")"] and c["\""] % 2 == 0


def run(filename, env=THE_GLOBAL_ENV):
    with open(filename, "r") as _file:
        return eval(_file.read(), env)


def load(filename, env=THE_GLOBAL_ENV):
    with open(filename, "r") as _file:
        eval(_file.read(), env)


def make_argparser():
    parser = ArgumentParser(description="loispy interpreter")
    parser.add_argument("file", nargs="?", default=None,
        help="A file to run directly")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug flag", default=False)
    parser.add_argument("-l", "--load", nargs="*", default=[],
        help="A list of files to eval before doing anything else.")
    return parser


def load_libs():
    load("./stdlib/builtinmacros.loisp", THE_GLOBAL_ENV)


def main():
    args = make_argparser().parse_args()
    load_libs()
    for f in args.load:
        load(f)
    if not args.file:
        repl(debug=args.debug)
    else:
        print to_string(run(args.file))


if __name__ == "__main__":
    main()
