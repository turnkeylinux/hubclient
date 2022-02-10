#!/usr/bin/python3
# Copyright (c) 2011-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNUI/Linux <admin@turnkeylinux.org> - all rights reserved

"""Update hub with server boot status"""

import sys

import hubclient_lib.conf as hubconf
import hubclient_lib.api as hubapi


def usage():
    print("Syntax: %s <boot_status> [ comment ]" % sys.argv[0], file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        usage()

    conf = hubconf.HubServerConf()
    serverid = conf.get('serverid')

    boot_status = args[0]
    try:
        comment = args[1]
    except:  # XXX TODO which exception(s)? [shouldn't use bare except]
        comment = None

    hubapi.Server().status(serverid, boot_status, comment)


if __name__ == "__main__":
    main()
