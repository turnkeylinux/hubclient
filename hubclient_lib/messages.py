# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

import os
import sys

from tklamq_lib.amqp import decode_message
from .exceptions import HubClientMsgError


def func_authorize_sshkey(sshkey):
    sshdir = "/root/.ssh"
    if not os.path.exists(sshdir):
        os.makedirs(sshdir)
        os.chmod(sshdir, 0o700)

    with open(os.path.join(sshdir, 'authorized_keys'), 'a') as fob:
        fob.write(sshkey + "\n")


def func_preseed_inithooks(value):
    arg, val = value.split("=", 1)
    val = val.lstrip()
    with open('/etc/inithooks.conf', "a") as fob:
        fob.write(f'export {arg}="{val}"\n')


def func_init_masterpass(masterpass):
    """deprecated: only used in legacy builds"""
    with open('/etc/inithooks.conf', "w") as fob:
        for s in ('rootpass', 'mysqlpass', 'pgsqlpass'):
            fob.write(f"export {s.upper()}={masterpass}\n")


def wrapper_callback(message_data, message):
    """generic message consume callback wrapper

    content must be of type dict, with key matching function to be called
    passing value:

        content = {'function1': 'argument for function1'}
        would call func_function1('argument for function1')

    will raise an exception if message is not encrypted
    """
    
    # always send acknowledgement, even if an exception is raised so as not
    # block the queue
    message.ack()

    if not message_data['encrypted']:
        raise HubClientMsgError("hubclient only accepts encrypted messages")

    secret = os.getenv('SECRET')
    sender, content, timestamp = decode_message(message_data, secret)
    
    for func_name in content.keys():
        func = getattr(sys.modules[__name__], 'func_' + func_name)
        func(content[func_name])
    
    print(f'message processed ({timestamp.isoformat(" ")})')
