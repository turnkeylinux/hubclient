import os
import sys
import tempfile

import executil
import simplejson as json
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

def wrapper_callback(message_data, message):
    """generic message consume callback wrapper

    deserializes message content after decryption and calls specified function
    with specified arguments, e.g.,

        content = {'script', '#!/bin/bash echo "hello world"'}

        would call _func_script('#!/bin/bash echo "hello world"')

    will raise an exception if message is not encrypted
    """
    
    # always send acknowledgement, even if an exception is raised so as not
    # block the queue
    message.ack()

    if not message_data['encrypted']:
        raise Error("hubclient only accepts encrypted messages")

    secret = os.getenv('SECRET')
    sender, content, timestamp = decode_message(message_data, secret)

    content_data = json.loads(content)
    for func_name in content_data.keys():
        func = getattr(sys.modules[__name__], 'func_' + func_name)
        func(content_data[func_name])
    
    print "message processed (%s)" % timestamp.isoformat(" ")

