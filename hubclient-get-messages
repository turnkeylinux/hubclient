#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

"""Consume and process messages from queue"""

import os
import sys

import hubclient_lib.conf as hubconf
from hubclient_lib.messages import wrapper_callback
from tklamq_lib.amqp import connect


def usage():
    print("Syntax: %s" % sys.argv[0], file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(1)


def fatal(s):
    print("error: " + str(s), file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) > 1:
        usage()

    if os.geteuid() != 0:
        fatal("hubclient requires root privileges to run")

    amqconf = hubconf.HubAMQConf()
    conf = hubconf.HubServerConf()
    conf.validate_required(['serverid', 'subkey', 'secret'])

    queue = f"server.{conf.subkey}.{conf.serverid}"

    conn = connect()
    conn.consume(queue, callback=wrapper_callback)


if __name__ == "__main__":
    main()
