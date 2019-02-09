import glob  # just import a random module, do not log in glob

def hello_name(name):
    print "hello %s from example1.py" % name # @log line 4, value of name


def add(x, y):
    result = x + y  # log @line 10, x, y and result values
    return result # log @line 9, x, y and result values

hello_name("donal") # log @line 11,
add(3, 2)

'''So I expect it to log import glob, but not log anything from
the glob module.
Then it will log it loads hello_name at line 3, loads add at line 7
Then it will log it's at line 11
Then line 3, 4, 4 back to 11
Then line 12, to 7, 8 and 9, 9 to 12
Then it may log this comment section, not sure.
'''