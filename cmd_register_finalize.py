#!/usr/bin/python
# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""Finalize server registration in hub (once server is approved)"""

import os
import sys

import hubapi
import hubconf

class Error:
    pass

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

    conf = hubconf.HubServerConf()
    conf.validate_required(['serverid'])

    subkey, secret = hubapi.Server.register_finalize(conf.serverid)

    conf.update({'subkey': subkey, 'secret': secret})
    conf.write()

    print "successful"

if __name__=="__main__":
    main()

