"""Tracer and Logbox"""
try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import datetime


class Logbox(object):
    """Logbox contains what has been traced in a big list of dict entries"""

    # default to a using a shared directory across instances of this class
    directory = "flight-recordings/"

    def __init__(self):
        self._box = []

    @staticmethod
    def extract_locals(frame):
        # I'm nearly sure co_names are really callables that could generate a new scope
        # Actually I'm not sure what they are...
        # It may be useful to take timings for every event because things like
        # sleeps are not easy to know otherwise...
        return {local: str(frame.f_locals.get(local)) for local in frame.f_code.co_varnames}

    @staticmethod
    def extract_names(frame):
        return {local: str(frame.f_locals.get(local)) for local in frame.f_code.co_names}

    def log_line(self, frame):
        info = {'event': 'line', 'line_no': frame.f_lineno,
                'scope': str(frame.f_code.co_name), 'locals': self.extract_locals(frame),
                'co_names': self.extract_names(frame)}
        self._box.append(info)

    def log_return(self, frame, arg):
        info = {'event': 'return', 'line_no': str(frame.f_lineno),
                'scope': str(frame.f_code.co_name), 'locals': self.extract_locals(frame),
                'return_value': str(arg), 'co_names': self.extract_names(frame)}
        self._box.append(info)

    def log_call(self, frame, arg):
        info = {'event': 'call', 'line_no': str(frame.f_lineno),
                'scope': str(frame.f_code.co_name), 'vars': self.extract_locals(frame),
                'call_value': str(arg), 'co_names': self.extract_names(frame)}
        self._box.append(info)

    def log_exception(self, frame, arg):
        info = {'event': 'exception', 'line_no': str(frame.f_lineno),
                'scope': str(frame.f_code.co_name), 'vars': self.extract_locals(frame),
                'exception_value': str(arg), 'co_names': self.extract_names(frame)}
        self._box.append(info)

    def pickle(self, logname=None):
        """Saves the contents of the log box to disk, by picking it.

        :param logname: what to call the logname. Defaults to using datetime stamp
            of time this function is called at.

        Will save the logbox into a directory in the cwd called 'flight-recordings'.
        The file-extension is saves it with is '.fb'

        Return path (str) to pickled file saved to disk.
        """
        directory = self.directory
        if not os.path.isdir(directory):
            # if it already exists but is a file, os should throw an error
            os.mkdir(directory)

        timestamp = datetime.datetime.now().strftime("%y-%m-%dT%H-%M-%S")
        default_logname = "%s%s.fb" % (directory, timestamp) 

        if logname is None:
            # nothing from caller, use default
            path = default_logname
        # caller is naming file
        elif logname[-3:] == ".fb":
            # filextension provided by caller
            path = "%s%s" % (directory, logname)
        else:
            # fileextension not provided by caller
            path = "%s%s.fb" % (directory, logname)

        # don't overwrite existing files, just put it somewhere else, i.e. the default
        # place
        if os.path.exists(path):
            print "WARNING path '%s' already exits, not going to overwrite it. " \
                "Using default timestamped value instead"
            path = default_logname

        with open(path, "wb") as box_file:
            pickle.dump(self._box, box_file)

        return path


class Tracer(object):
    def __init__(self, target):
        """target is module name we want to trace, other py modules will
        be excluded from the tracing"""
        self.target = target + ".py"
        self.box = Logbox()

    def hook(self, frame, event, arg):
        self.box.log_call(frame, arg)
        # self.target is just the last part of the path
        # whereas co_filename is probably the whole path
        if self.target in frame.f_code.co_filename:
            # Good, we are in the module we want to trace
            # Log the line we are at and return the tracer
            return self.tracer
        else:
            # Else don't hook this, do nothing
            return None

    def tracer(self, frame, event, arg):
        # print event
        if self.target not in frame.f_code.co_filename:
            return None  # if we aren't the target file do nothing
        else:
            if event == 'line':
                self.box.log_line(frame)
            elif event == 'call':
                self.box.log_call(frame, arg)
            elif event == 'return':
                self.box.log_return(frame, arg)
            elif event == 'exception':
                # Note it is unhandled exceptions we care about more
                # than normal exceptions. We haven't detected whether 
                # it is unhandled yet, nor have we written a wrapper
                # for catching them.
                self.box.log_exception(frame, arg)
            else:
                # Nothing else is interesting, ignoring c functions atm
                return None
