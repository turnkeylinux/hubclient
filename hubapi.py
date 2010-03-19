# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""
Environment variables:

    HUB_APIURL          default: https://hub.turnkeylinux.org/api
"""

import os
import pycurl
import urllib
import cStringIO

import simplejson as json
import hubconf

URL = os.getenv('HUB_APIURL', 'https://hub.turnkeylinux.org/api')

class HubAPIError(Exception):
    pass

def _post(uri, post_data={}):
    response = {}
    response_data = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, URL + "/" + uri)
    c.setopt(c.POSTFIELDS, urllib.urlencode(post_data))
    c.setopt(c.WRITEFUNCTION, response_data.write)
    #c.setopt(c.VERBOSE, 1)
    c.perform()

    response['code'] = c.getinfo(pycurl.RESPONSE_CODE)
    response['type'] = c.getinfo(pycurl.CONTENT_TYPE)
    c.close()

    response['data'] = response_data.getvalue()
    response_data.close()

    return response

def register_finalize():
    """final phase of server registration in hub"""
    conf = hubconf.HubClientConf()
    conf.validate_required(['serverid'])

    response = _post('server/register/finalize/', {'serverid': conf.serverid})

    if not response['code'] == 200:
        raise HubAPIError(response)

    data = json.loads(response['data'])
    conf.update(data)
    conf.write()

