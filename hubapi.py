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

from pycurl_wrapper import API

class Error(Exception):
    pass

class Server:
    API_URL = 'https://hub.turnkeylinux.org/api/server/'

    Error = Error

    def __init__(self):
        self.api = API()

    def register_finalize(self, serverid):
        url = self.API_URL + "register/finalize/"
        attrs = {'serverid': serverid}

        response = self.api.request('POST', url, attrs)
        return response['subkey'], response['secret']

    def status(self, serverid, boot_status):
        url = self.API_URL + "status/%s/" % boot_status
        attrs = {'serverid': serverid}

        # workaround PUT issue: http://redmine.lighttpd.net/issues/1017
        response = self.api.request('PUT', url, attrs)
        return response
