#!/usr/bin/python
# Copyright (c) 2011 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""Update hub that server is booted (depreciated: backwards compat.)"""

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

    boot_status = "booted"
    hubapi.Server().status(conf.serverid, boot_status)
    print "Successfully updated Hub with server boot status: %s" % boot_status

if __name__=="__main__":
    main()

