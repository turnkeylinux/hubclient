# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved

"""TurnKey Hub API - Server

Notes:
    - Default URL: https://hub.turnkeylinux.org/api/server/
    - Responses are returned in application/json format

register/finalize/
    method: POST
    fields: serverid
    return: subkey, secret

status/booted/
    method: PUT
    fields: serverid
    return: <response_code>

Exceptions::

    400 Request.MissingArgument
    404 HubServer.NotFound
    401 HubServer.NotApproved
    401 HubServer.Finalized
"""

import simplejson as json

from pycurl_wrapper import Curl

class Error(Exception):
    pass

class API:
    ALL_OK = 200
    CREATED = 201
    DELETED = 204

    @classmethod
    def request(cls, method, url, attrs={}, headers={}):
        c = Curl(url, headers)
        func = getattr(c, method.lower())
        func(attrs)

        if not c.response_code in (cls.ALL_OK, cls.CREATED, cls.DELETED):
            name, description = c.response_data.split(":", 1)
            raise Error(c.response_code, name, description)

        return json.loads(c.response_data)

class Server:
    API_URL = 'https://hub.turnkeylinux.org/api/server/'
    API_HEADERS = {'Accept': 'application/json'}

    Error = Error

    @classmethod
    def register_finalize(cls, serverid):
        url = cls.API_URL + "register/finalize/"
        attrs = {'serverid': serverid}

        response = API.request('POST', url, attrs, cls.API_HEADERS)
        return response['subkey'], response['secret']

    @classmethod
    def status(cls, serverid, boot_status):
        url = cls.API_URL + "status/%s/" % boot_status
        attrs = {'serverid': serverid}

        # workaround PUT issue: http://redmine.lighttpd.net/issues/1017
        headers = cls.API_HEADERS.copy()
        headers['Expect'] = ''

        response = API.request('PUT', url, attrs, headers)
        return response
