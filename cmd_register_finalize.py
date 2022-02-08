#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/linux <admin@turnkeylinux.org> - all rights reserved

"""Finalize server registration in hub (once server is approved)"""

import os
import sys

import hubclient_lib


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

    conf = hubclient_lib.conf.HubServerConf()
    conf.validate_required(['serverid'])

    subkey, secret = hubclient_lib.api.Server().register_finalize(
            conf.serverid)

    conf.update({'subkey': subkey, 'secret': secret})
    conf.write()

    print("Successfully finalized server registration with the Hub")


if __name__ == "__main__":
    main()
