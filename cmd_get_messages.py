#!/usr/bin/python
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

def main():
    if len(sys.argv) > 1:
        usage()

    amqconf = hubconf.HubAMQConf()
    conf = hubconf.HubClientConf()
    conf.validate_required(['serverid', 'apikey', 'secret'])

    queue = "server.%s.%s" % (conf.apikey, conf.serverid)

    conn = connect()
    conn.consume(queue, callback=wrapper_callback)

if __name__=="__main__":
    main()

