#!/usr/bin/python
# Copyright (c) 2011 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""Update hub that server is booted"""

import sys

import hubapi
import hubconf

class Error:
    pass

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    conf = hubconf.HubServerConf()
    conf.validate_required(['serverid'])

    hubapi.Server.status_booted(conf.serverid)
    print "Successfully updated Hub that server has booted"

if __name__=="__main__":
    main()

