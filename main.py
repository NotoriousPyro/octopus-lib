import asyncio
import datetime

from octopus.client import OctopusClient
from octopus.models import ConsumptionRequestParams, OctopusConfig


async def main():
    client = OctopusClient(config=OctopusConfig.parse_file("config.json"))
    async for data in client.get_meter_consumption_data(
        params=ConsumptionRequestParams(
            period_from=datetime.datetime.now() - datetime.timedelta(days=7),
            page_size=200,
        )
    ):
        print(data)


if __name__ == "__main__":
    asyncio.run(main())
