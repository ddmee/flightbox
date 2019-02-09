"""LineByLine takes a flightbox trace and converts it to a log file.

The log file is a recording of things that a person debugging the program,
who wants to know what happened, would like to know.

The way I debug a program is I begin at a line and then step my way
through a program. Looking at what the values of local variables are, when
a function is called and when a function returns.

I am primarily interested in knowing which line the program is at, when
it calls and returns to another function, and when a variable on that line changes
value.

This aims to produce such a line-by-line recount of the programs execution
from the flightbox recording.
"""
import os
try:
    import cpickle as pickle
except ImportError:
    import pickle
from pprint import pprint


class LineByLine(object):
    """Creates a line-by-line logfile from a flightbox.

    It puts the .log file into the directory 'linebyline',
    in a file of the same name as the flightbox, except with
    the filename extension '.log' inplace of '.fb'
    """
    def __init__(self, flightbox):
        """
        :param flightbox: should be the extact path to the flightbox. Please
            make sure this is a real path etc before passing to this function.
        """
        assert os.path.isfile(flightbox)
        head, tail = os.path.split(flightbox)
        assert os.path.isdir(head)
        name, fb_ext = os.path.splitext(tail)
        assert fb_ext == ".fb", "flightbox filename lacks .fb extension? '%s'" \
            % tail

        self.directory = os.path.join(os.path.dirname(head), "linebyline")
        self.path = os.path.join(self.directory, name, ".log")

        if os.path.exists(self.path):
            # don't want to overwrite and no default path to fall back on,
            # wouldn't want to accidentally overwrite a trace file.
            raise EnvironmentError("file already exists at %s" % self.path)

        with open(flightbox, "rb") as incoming_box:
            # box should be a big list of dic entries
            self.box = pickle.load(incoming_box)
 
    def process(self):
        """ """
        pass

    def barf(self):
        """Prints out the raw flightbox to the console.
        Does not interpret linebyline stuff. Use process and write for that.
        Returns None.
        """
        pprint(self.box)

    def write(self):
        """Call to convert flightbox to a line-by-line log.

        Returns (str) path of linebyline.log that was created.
        """
        if not os.path.isdir(self.directory):
            # if it already exists as a file, the os should throw an error
            # at least windows does
            os.mkdir(self.directory)
