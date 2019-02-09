# stdlib
import argparse
from importlib import import_module
# from pprint import pprint
import sys
# local
from src.tracer import Tracer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module_to_import")
    args = parser.parse_args()
    tracer = Tracer(args.module_to_import)
    # hack on the path... just so the examples in test dir work
    sys.path.append("C:\\Users\\meedo\\code\\flightbox\\test")
    # actually set the hook, but do it before importing the example
    # module.
    sys.settrace(tracer.hook)

    # this import is equivalent of running a module given how example are structured
    import_module(args.module_to_import)

    # stop the hook, probably not required
    sys.settrace(None)

    # save it to disk
    tracer.box.pickle()


if __name__ == '__main__':
    main()
