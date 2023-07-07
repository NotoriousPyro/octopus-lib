import aiohttp
import asyncio

from typing import Any, Generator

from .session import OctopusSession
from .models import (
    ConsumptionRequestParams,
    ConsumptionResponseModel,
    ElectricOrGasUrlMapping,
    Meter,
    OctopusConfig,
)


BASE_URL = "https://api.octopus.energy"

# logging.basicConfig(level=logging.DEBUG)


class OctopusClient:
    def __init__(self, config: OctopusConfig) -> None:
        self.config = config

    def __url_for__(self, meter: Meter):
        return ElectricOrGasUrlMapping[meter.type].format(
            mpn=meter.mpn, serial=meter.serial
        )

    async def __get_session__(self) -> OctopusSession:
        return OctopusSession(
            auth=aiohttp.BasicAuth(login=self.config.api_key),
            base_url=BASE_URL,
            connector=aiohttp.TCPConnector(),
        )

    async def get_meter_consumption_data(
        self, *, params: ConsumptionRequestParams = ConsumptionRequestParams()
    ) -> Generator[ConsumptionResponseModel, Any, None]:
        async with await self.__get_session__() as session:
            response: ConsumptionResponseModel
            for response in await asyncio.gather(
                *(
                    asyncio.wait_for(
                        session.get(
                            ConsumptionResponseModel,
                            url=self.__url_for__(meter),
                            params=params,
                        ),
                        timeout=600,
                    )
                    for meter in self.config.meters
                )
            ):
                yield response
