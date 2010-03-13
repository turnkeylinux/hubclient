import os
import sys
import tempfile

import executil
from tklamq.amqp import decode_message

class Error(Exception):
    pass

class TempFile(file):
    def __init__(self, prefix='tmp', suffix=''):
        fd, path = tempfile.mkstemp(suffix, prefix)
        os.close(fd)
        self.path = path
        self.pid = os.getpid()
        file.__init__(self, path, "w")

    def __del__(self):
        if self.pid == os.getpid():
            os.remove(self.path)

def func_script(content):
    """execute content as script
    
    will raise exception if
        - RUN_SCRIPTS environment variable is not True
        - content does not start with shebang
    """
    run_scripts = os.getenv('RUN_SCRIPTS', 'false')
    if not run_scripts.lower() == "true":
        raise Error("will not execute, run_scripts not enabled:\n%s" % content)

    if not content.startswith("#!"):
        raise Error("will not execute, shebang not specified:\n%s" % content)

    fh = TempFile()
    fh.writelines(content)
    fh.close()

    os.chmod(fh.path, 0750)
    executil.system(fh.path)

def func_init_masterpass(masterpass):
    """set initial passwords using master password by creating inithooks.conf
    will be depreciated when the hub supports custom appliance configuration
    """

    print masterpass
    fh = file('/tmp/inithooks.conf', "w")
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

