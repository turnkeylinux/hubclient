# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved


class HubClientError(Exception):
    pass


class HubClientMsgError(HubClientError):
    pass


class HubClientApiError(HubClientError):
    pass
