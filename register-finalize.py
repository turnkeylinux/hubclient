#!/usr/bin/python
"""Finalize server registration in hub (once server is approved)"""

import sys
import hubapi

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    error = hubapi.register_finalize()
    if error:
        fatal(error)

    print "successful"

if __name__=="__main__":
    main()

