class UnexpectedResponse(Exception):
    pass


class InvalidAccount(UnexpectedResponse):
    pass


class InvalidToken(UnexpectedResponse):
    pass


class InvalidProxy(Exception):
    """raises when proxy check failed"""

    pass
