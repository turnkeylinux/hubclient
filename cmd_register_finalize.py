#!/usr/bin/python
"""Finalize server registration in hub (once server is approved)"""

import os
import sys

import hubapi

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    if os.geteuid() != 0:
        fatal("hubclient requires root privileges to run")

    hubapi.register_finalize()
    print "successful"

if __name__=="__main__":
    main()

