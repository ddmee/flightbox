import datetime
import time


class Stopwatch(object):
    """A simple stopwatch counting in seconds."""
    def __init__(self):
        self._start_time = None
        self._stop_time = None

    def start(self):
        """Call to start the clock. Must be called before stop"""
        if self._start_time or self._stop_time:
            raise RuntimeError("Timer has already been started once")
        else:
            self._start_time = datetime.datetime.now()

    def stop(self):
        """Call to stop the clock."""
        if not self._start_time:
            raise RuntimeError("Timer has not been started")
        elif self._stop_time:
            raise RuntimeError("Timer has already been stopped")
        else:
            self._stop_time = datetime.datetime.now()

    def total(self):
        """Returns difference between start and stop time in seconds.
        Returns a float"""
        if self._start_time is None:
            raise RuntimeError("Timer has not been started")
        elif self._stop_time is None:
            raise RuntimeError("Timer has not been stopped")
        else:
            result = (self._stop_time - self._start_time).total_seconds(); return result


clock = Stopwatch()
clock.start()
time.sleep(1)
clock.stop()
timed = clock.total()
print "Spent %s seconds" % timed


'''So I expect it to log ...
# The reason 'start' and 'stop' and 'sleep' are here is that they are codeobject that
# are going to be called in the current scope (currently the module frame). But they
# haven't been initalised to anything yet. It includes any object, so the 'object' value
# is included. But keywords like 'print' or 'class' are not code objects.
line 1, local {}, callables {stopwatch:none, time:none, datetime:(pointer), start:none, stop:none, sleep:none, total:none, clock:none, object: None}, scope module
line 2, += callable {time: pointer}
line 5, class declaration causes interpret to load the functions of the class, like getting pointer to __init__ , start, stop
It then return the declared class back to the calling scope, to fill in the local variable for Stopwatch
line 38, ? should jump to line 7
line 7, scope: __init__, callables (_start_time: None, _stop_time: None), locals {self}
line 9 back to line 38, as return value from __init__ is None
line 38: scope: module, callables (clock: instanceofstopwatch)
line 39 will jump to line 11
# co_names is basically any reference object within a scope it seems
line 11 scope: start, callables (_starttime, _stoptime, datetime, now, runtimerror), locals {self}
line 13 is branch, so jumps to line 16
line 16, callabe _starttime is set to instance of datetime ## THIS DID NOT HAPPEN, _starttime remained None!!!! (ahh)
line 16 return value none, jumps to line 40
line 40 sleeps
line 41, to line 18, 
line 18 scope:stop,  callabes must now be (_starttime: datetimeobject). NOPE! co_names must be callables rather than values. The values must be within self on locals
line 20 false, jump to line 22 - false, jump to line 25
line 25
line 25 return value none

line 25 return value is like '2.012' or whatever, what are the locals at this point for timed, none until
jump to line 42, timed is set to 2.021, at least by line 43

'''