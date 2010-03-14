#!/usr/bin/python
"""Send heartbeat message to hub"""

import os
import sys

import hubconf
from tklamq.amqp import connect, encode_message

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
    conf = hubconf.HubClientConf()
    conf.validate_required(['serverid'])

    conn = connect()
    conn.publish(exchange="hub", routing_key="hub.heartbeat",
                 message=encode_message(sender=conf.serverid, content=""),
                 persistent=False)


if __name__=="__main__":
    main()

