#!/usr/bin/python
# Copyright (c) 2011 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""Update hub with server boot status"""

import sys

import hubapi
import hubconf

class Error:
    pass

def usage():
    print >> sys.stderr, "Syntax: %s <boot_status>" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if not len(sys.argv) == 2:
        usage()

    conf = hubconf.HubServerConf()
    conf.validate_required(['serverid'])

    boot_status = sys.argv[1]
    hubapi.Server().status(conf.serverid, boot_status)
    print "Successfully updated Hub with server boot status: %s" % boot_status

if __name__=="__main__":
    main()

