"""
Environment variables:

    HUB_SERVERCONF      default: /etc/hubclient/server.conf

    BROKER_HOST         default: amq.turnkeylinux.org
    BROKER_PORT         default: 5672
    BROKER_USER         default: server
    BROKER_PASSWORD     default: server
    BROKER_VHOST        default: /hub
"""

import os

class ConfFileError(Exception):
    pass

class ConfFile(dict):
    """Configuration file class (targeted at simple shell type configs)

    Usage:

        class foo(ConfFile):
            CONF_FILE = /path/to/conf
            REQUIRED = ['arg1' ,'arg2']

        print foo.arg1      # display ARG1 value from /path/to/conf
        foo.arg2 = value    # set ARG2 value
        foo.write()         # write new/update config to /path/to/conf

    """
    CONF_FILE = None
    REQUIRED = []
    SET_ENVIRON = False

    def __init__(self):
        self.read()
        self.validate_required()
        if self.SET_ENVIRON:
            self.set_environ()

    def validate_required(self, required=[]):
        """raise exception if required arguments are not set
        REQUIRED validated by default, but can be optionally extended
        """
        self.REQUIRED.extend(required)
        for attr in self.REQUIRED:
            if not self.has_key(attr):
                error = "%s not specified in %s" % (attr.upper(), self.CONF_FILE)
                raise ConfFileError(error)

    def set_environ(self):
        """set environment (run on initialization if SET_ENVIRON)"""
        for key, val in self.items():
            os.environ[key.upper()] = val

    def read(self):
        if not self.CONF_FILE or not os.path.exists(self.CONF_FILE):
            return 

        for line in file(self.CONF_FILE).readlines():
            line = line.rstrip()

            if not line or line.startswith("#"):
                continue

            key, val = line.split("=")
            self[key.strip().lower()] = val.strip()

    def write(self):
        fh = file(self.CONF_FILE, "w")
        items = self.items()
        items.sort()
        for key, val in items:
            print >> fh, "%s=%s" % (key.upper(), val)

        fh.close()

    def items(self):
        items = []
        for key in self:
            items.append((key, self[key]))

        return items

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, e:
            raise AttributeError(e)

    def __setattr__(self, key, val):
        self[key] = val

class HubServerConf(ConfFile):
    SET_ENVIRON = True
    CONF_FILE = os.getenv('HUB_SERVERCONF', '/etc/hubclient/server.conf')

class HubAMQConf(dict):
    def __init__(self):
        self['broker_host'] = os.getenv('BROKER_HOST', 'amq.turnkeylinux.org')
        self['broker_port'] = os.getenv('BROKER_PORT', '5672')
        self['broker_user'] = os.getenv('BROKER_USER', 'server')
        self['broker_password'] = os.getenv('BROKER_PASSWORD', 'server')
        self['broker_vhost'] = os.getenv('BROKER_VHOST', '/hub')

        for key in self:
            os.environ[key.upper()] = self[key]

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, e:
            raise AttributeError(e)

    def __setattr__(self, key, val):
        self[key] = val

