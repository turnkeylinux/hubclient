"""
Environment variables:

    HUBCLIENT_CONF      default: /etc/hubclient.conf

    BROKER_HOST         default: amq.turnkeylinux.org
    BROKER_PORT         default: 5672
    BROKER_USER         default: server
    BROKER_PASSWORD     default: server
    BROKER_VHOST        default: /hub
"""

import os
from conffile import ConfFile

class HubClientConf(ConfFile):
    SET_ENVIRON = True
    CONF_FILE = os.getenv('HUBCLIENT_CONF', '/etc/hubclient.conf')

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

