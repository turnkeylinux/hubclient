#!/usr/bin/python
# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""Consume and process messages from queue"""

import os
import sys

import hubconf
from hubmessages import wrapper_callback
from tklamq.amqp import connect

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

    amqconf = hubconf.HubAMQConf()
    conf = hubconf.HubServerConf()
    conf.validate_required(['serverid', 'apikey', 'secret'])

    queue = "server.%s.%s" % (conf.apikey, conf.serverid)

    conn = connect()
    conn.consume(queue, callback=wrapper_callback)

if __name__=="__main__":
    main()

