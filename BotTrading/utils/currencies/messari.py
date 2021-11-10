import asyncio
import aiohttp


class MessariApi:
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()


async def main():
    api = MessariApi()
    json = await api.get_asset_metrics("eur", "market_data")
    print(json)


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)
