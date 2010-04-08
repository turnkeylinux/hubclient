# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

import os
import sys

from tklamq.amqp import decode_message

class Error(Exception):
    pass

def func_init_masterpass(masterpass):
    """set initial passwords using master password by creating inithooks.conf
    will be depreciated when the hub supports custom appliance configuration
    """

    fh = file('/etc/inithooks.conf', "w")
    for s in ('rootpass', 'mysqlpass', 'pgsqlpass'):
        print >> fh, "export %s=%s" % (s.upper(), masterpass)

    fh.close()

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
        raise Error("hubclient only accepts encrypted messages")

    secret = os.getenv('SECRET')
    sender, content, timestamp = decode_message(message_data, secret)
    
    for func_name in content.keys():
        func = getattr(sys.modules[__name__], 'func_' + func_name)
        func(content[func_name])
    
    print "message processed (%s)" % timestamp.isoformat(" ")

