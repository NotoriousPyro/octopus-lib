import aiohttp
import datetime

from aiohttp.typedefs import StrOrURL
from pydantic import parse_obj_as
from typing_extensions import override
from typing import Any, Type, Sequence, Mapping

from octopus.models import BaseRequestParams, T


def dict_to_str(obj: Any):
    if isinstance(obj, dict):
        return {k: dict_to_str(obj.get(k)) for k in obj}
    if isinstance(obj, datetime.datetime):
        return obj.strftime(r"%Y-%m-%dT%H:%M:%S")
    return obj


ConvertibleParamValues = str | int | float
QueryParams = Mapping[
    str, ConvertibleParamValues | Sequence[ConvertibleParamValues] | None
]


class OctopusSession(aiohttp.ClientSession):
    @override
    async def get(
        self,
        type: Type[T],
        *,
        url: StrOrURL,
        allow_redirects: bool = True,
        params: BaseRequestParams
    ) -> T:
        async with super().get(
            url,
            allow_redirects=allow_redirects,
            params=dict_to_str(params.dict(exclude_none=True)),
        ) as response:
            return parse_obj_as(type, await response.json())

    @override
    async def __aenter__(self) -> "OctopusSession":
        return self
