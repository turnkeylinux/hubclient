#!/usr/bin/python
"""Send heartbeat message to hub"""

import sys

import hubconf
from tklamq.amqp import connect, encode_message

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    amqconf = hubconf.HubAMQConf()
    conf = hubconf.HubClientConf()
    conf.validate_required(['serverid'])

    conn = connect()
    conn.publish(exchange="hub", routing_key="hub.heartbeat",
                 message=encode_message(sender=conf.serverid, content=""),
                 persistent=False)


if __name__=="__main__":
    main()

