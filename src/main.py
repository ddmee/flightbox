import argparse
import sys
from importlib import import_module
from pprint import pprint as pprint

GLOBAL_LIST = []

def extract_locals(frame):
    return {local: frame.f_locals.get(local) for local in frame.f_code.co_varnames}

def extract_names(frame):
    return {local: frame.f_locals.get(local) for local in frame.f_code.co_names}

def log_line(frame):
    info = {'event': 'line', 'line_no': frame.f_lineno,
    'scope': frame.f_code.co_name, 'locals': extract_locals(frame),
    'co_names': extract_names(frame)}
    GLOBAL_LIST.append(info)


def log_return(frame, arg):
    info = {'event': 'return', 'line_no': frame.f_lineno,
    'scope': frame.f_code.co_name, 'locals': extract_locals(frame),
    'return_value': arg, 'co_names': extract_names(frame)}
    GLOBAL_LIST.append(info)

def log_call(frame, arg):
    info = {'event': 'call', 'line_no': frame.f_lineno,
    'scope': frame.f_code.co_name, 'vars': extract_locals(frame),
    'call_value': arg, 'co_names': extract_names(frame)}
    GLOBAL_LIST.append(info)


def log_exception(frame, arg):
    info = {'event': 'exception', 'line_no': frame.f_lineno,
    'scope': frame.f_code.co_name, 'vars': extract_locals(frame),
    'exception_value': arg, 'co_names': extract_names(frame)}
    GLOBAL_LIST.append(info)


class Tracer(object):
    def __init__(self, target):
        """target is module name we want to trace, other py modules will
        be excluded from the tracing"""
        self.target = target + ".py"

    def hook(self, frame, event, arg):
        # self.target is just the last part of the path
        # whereas co_filename is probably the whole path
        if self.target in frame.f_code.co_filename:
            # Good, we are in the module we want to trace
            # Log the line we are at and return the tracer
            log_line(frame)
            return self.tracer
        else:
            # Else don't hook this, do nothing
            return None

    def tracer(self, frame, event, arg):
        if self.target not in frame.f_code.co_filename:
            return None # if we aren't the target file do nothing
        else:
            if event == 'line':
                log_line(frame)
            elif event == 'call':
                log_call(frame, arg)
            elif event == 'return':
                log_return(frame, arg)
            elif event == 'exception':
                # Note it is unhandled exceptions we care about more
                # than normal exceptions. We haven't detected whether 
                # it is unhandled yet, nor have we written a wrapper
                # for catching them.
                log_exception(frame, arg)
            else:
                # Nothing else is interesting, ignoring c functions atm
                return None



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("module_to_import")
    args = parser.parse_args()
    tracer = Tracer(args.module_to_import)
    # hack on the path...
    sys.path.append("C:\\Users\\meedo\\code\\flightbox\\test")
    sys.settrace(tracer.hook)
    import_module(args.module_to_import)
    for x in GLOBAL_LIST:
        pprint(x)
        print "\n"


if __name__ == '__main__':
    main()