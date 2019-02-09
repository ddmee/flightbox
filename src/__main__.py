# stdlib
import argparse
from glob import iglob
from importlib import import_module
import os
# from pprint import pprint
import sys
# local
from src.tracer import Tracer, Logbox
from src.linebyline import LineByLine


def fb_paths(directory, by_last_write=True):
    """Returns list of .fb files in a directory.

    :param directory: path (str) to search for .fb files

    :opt param by_last_write: sort list of paths by the time
        the fiile was last modified. Newest at 0, oldest at end.

    Just checks file exists and is a .fb, does not valid whether
    content is really a flightbox trace.

    Returns a list of (str) paths that are .fb files
    """
    assert os.path.isdir(directory)
    glob_pattern = os.path.join(directory, "*.fb")
    ordered_paths = map(
        os.path.normpath, 
        sorted(
            filter(os.path.isfile, iglob(glob_pattern)),
            lambda a, b: b - a,
            key=lambda x: int(os.path.getmtime(x))
        )
    )
    return ordered_paths


## EXECUTORS
def rec_executor(module):
    """Executes the rec subcommand

    :param module: str of python module name to import and trace
        execution of.

    Returns None.
    """
    tracer = Tracer(module)
    # hack on the path... just so the examples in test dir work
    sys.path.append("C:\\Users\\meedo\\code\\flightbox\\test")
    # actually set the hook, but do it before importing the example
    # module.
    sys.settrace(tracer.hook)

    # this import is equivalent of running a module given how example are structured
    import_module(module)

    # stop the hook, probably not required
    sys.settrace(None)

    # save it to disk
    flightrecording = tracer.box.pickle()
    print "\nSAVED flightbox to %s" % flightrecording


def replay_executor(flightbox=None, barf=False):
    """Executes replay subcommand

    :opt param flightbox: path to a flightbox trace to replay. If
        supply a str beginning with '~', you can use an index after
        it instead of a pathname. ~0 is the latest recording, ~1 is
        the second oldest, etc.

    :opt param barf: bool, if True, will not convert to line-by-line
        but will instead just print the contents of the flightbox
        to the console.

    Returns None.
    """
    if not flightbox:
        print "Defaulting to latest flightbox"
        index = 0
        # get the default directory, list all flightboxes and
        # use the most recently written.
        fb_path = fb_paths(Logbox.directory)[index]
    elif flightbox[0] == "~":
        # Caller has passed us an index. 0 is the latest
        # Strip arg of # and convert remainder to an index
        index = int(flightbox[1:])
        fb_path = fb_paths(Logbox.directory)[index]
    else:
        # actual flightbox name
        if not os.path.isfile(flightbox):
            raise EnvironmentError("Unable to find fb at '%s"
                                   % flightbox)
        elif os.path.splitext(flightbox)[1] != '.fb':
            raise EnvironmentError(
                "File at '%s' does not end with .fb" % flightbox)
        else:
            # confirm path and file with .fb
            fb_path = flightbox

    print "Found %s" % fb_path
    lbl = LineByLine(fb_path)
    if barf:
        lbl.barf()
    else:
        pass


## HANDLERS
def rec_handler(arg_namespace):
    _args = {
        "module": arg_namespace.module
    }
    return rec_executor(**_args)


def replay_handler(arg_namespace):
    _args = {
        "flightbox": arg_namespace.flightbox,
        "barf": arg_namespace.barf
    }
    return replay_executor(**_args)


def setup_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Rec subcommand parser
    rec_parser = subparsers.add_parser("rec",
        help="record code execution")
    rec_parser.add_argument("module")
    rec_parser.set_defaults(func=rec_handler)

    # replay subcommand parser
    replay_parser = subparsers.add_parser("replay", 
        help="step through a recorded trace/flightbox")
    replay_parser.add_argument("flightbox",
        help="path to flightbox trace, should be a .fb file. "
             "Can use indexes from 0 if start arg with '~'")
    replay_parser.add_argument("--raw", "--barf",
        dest="barf",
        action="store_true",
        help="just spits out the raw flightbox contents to console")
    replay_parser.set_defaults(func=replay_handler)

    return parser


def execute_cmdline():
    parser = setup_parser()
    args = parser.parse_args()
    # call subcommands handler
    args.func(args)


if __name__ == '__main__':
    execute_cmdline()
