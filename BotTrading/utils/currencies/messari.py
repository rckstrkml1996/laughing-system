import aiohttp

from .exceptions import (
    BadRequest,
    InvalidParam,
    Unauthorized,
    Forbidden,
    RateLimit,
    InternalError,
)


class MessariApi:
    def __init__(self, api_key: str = None):
        # self._api_key = api_key
        self.headers = None
        if api_key is not None:
            self.headers = {"x-messari-api-key": api_key}

    async def get_asset_metrics(self, asset_key: str, fields: str = None):
        """
        assetKey, string
        This "key" can be the asset's ID (unique), slug (unique), or symbol (non-unique)
        fields, string
        pare down the returned fields (comma , separated, drill down with a slash /)
        """
        url = f"https://data.messari.io/api/v1/assets/{asset_key}/metrics"
        params = {}
        if isinstance(fields, list):
            params["fields"] = ",".join(fields)
        elif isinstance(fields, str):
            params["fields"] = fields
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=params) as response:
                json = await response.json()
                if response.status == 200:
                    return json
                elif response.status == 400:
                    raise InvalidParam(json["status"]["error_message"])
                elif response.status == 401:
                    raise Unauthorized(json["status"]["error_message"])
                elif response.status == 403:
                    raise Forbidden(json["status"]["error_message"])
                elif response.status == 429:
                    raise RateLimit(json["status"]["error_message"])
                elif response.status == 500:
                    raise InternalError(json["status"]["error_message"])
                else:
                    raise BadRequest("somethink went wrong")
