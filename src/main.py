from parsing import parse
from analysis import analyze
from environment import make_global_env
import sys
import traceback
from utils import to_string
from argparse import ArgumentParser


def _exec(_str, env):
    return analyze(parse(_str))(env)


def repl(env):
    # TODO: multiline, nicer REPL. Tab-completion
    def ask():
        try:
            _str = raw_input("=> ")
        except KeyboardInterrupt:
            print "bye"
            sys.exit(0)
        try:
            val = _exec(_str, env)
        except Exception as e:
            val = "%s: %s" % (type(e).__name__, str(e))
            print traceback.format_exc()
        if val is not None:
            print to_string(val)
    print "===============\nlois.py v.0.0.1\n==============="
    while True:
        ask()


def run_file(f, env):
    with open(f, "r") as _file:
        print _exec(_file.read(), env)


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
        run_file(f, env)
    if not args.file:
        repl(env, args.debug)
    else:
        run_file(args.file, env)


if __name__ == "__main__":
    main()
