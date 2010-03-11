#!/usr/bin/python
"""Send heartbeat message to hub"""

import sys

import hubconf
from executil import system

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    amqconf = hubconf.HubAMQConf()
    srvconf = hubconf.HubServerConf()
    srvconf.validate_required(['serverid'])

    exchange = "hub"
    routing_key = "hub.heartbeat"
    system("tklamq-publish --sender=%s --non-persistent %s %s" % (srvconf.serverid,
                                                                  exchange,
                                                                  routing_key))

if __name__=="__main__":
    main()

