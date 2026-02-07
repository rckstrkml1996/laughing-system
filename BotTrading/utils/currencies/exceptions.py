class NoCurrenciesError(Exception):
    pass


class BadRequest(Exception):
    pass


class InvalidParam(BadRequest):
    """400"""

    pass


class Unauthorized(BadRequest):
    """401"""

    pass


class Forbidden(BadRequest):
    """403"""

    pass


class RateLimit(BadRequest):
    """429"""

    pass


class InternalError(BadRequest):
    """500"""

    pass
