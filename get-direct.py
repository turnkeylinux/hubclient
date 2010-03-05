#!/usr/bin/python
"""Consume and process messages from queue"""

import os
import sys

import hubconf
import executil

def usage():
    print >> sys.stderr, "Syntax: %s" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    amqconf = hubconf.HubAMQConf()
    srvconf = hubconf.HubServerConf()
    srvconf.validate_required(['serverid', 'apikey', 'secret'])

    os.environ['TKLAMQ_SECRET'] = srvconf.secret

    queue = "server.%s.%s" % (srvconf.apikey, srvconf.serverid)
    executil.system("tklamq-consume %s" % queue)

if __name__=="__main__":
    main()

