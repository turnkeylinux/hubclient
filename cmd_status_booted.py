#!/usr/bin/python3
# Copyright (c) 2011-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

"""Update hub that server is booted (depreciated: backwards compat.)"""

import sys

import hubclient_lib

def usage():
    print("Syntax: %s" % sys.argv[0], file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) > 1:
        usage()

    conf = hubclient_lib.conf.HubServerConf()
    conf.validate_required(['serverid'])

    boot_status = "booted"
    hubclient_lib.api.Server().status(conf.serverid, boot_status)
    print(f"Successfully updated Hub with server boot status: {boot_status}")

if __name__ == "__main__":
    main()
