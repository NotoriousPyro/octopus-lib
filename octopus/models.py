import datetime

from enum import StrEnum
from pydantic import BaseModel
from typing import List, TypeVar, Generic


class ResultsFieldConsumptionResponseModel(BaseModel):
    consumption: float
    interval_start: datetime.datetime
    interval_end: datetime.datetime


T = TypeVar("T")


class BaseResponseModel(BaseModel, Generic[T]):
    count: int | None
    next: str | None
    previous: str | None
    results: List[T] | None


class ConsumptionResponseModel(BaseResponseModel[ResultsFieldConsumptionResponseModel]):
    ...


class BaseRequestParams(BaseModel):
    period_from: datetime.datetime | None
    period_to: datetime.datetime | None
    page_size: int | None


class ConsumptionRequestParams(BaseRequestParams):
    order_by: str | None
    group_by: str | None


class ElectricOrGas(StrEnum):
    electricity = "electricity"
    gas = "gas"


ElectricOrGasUrlMapping = {
    ElectricOrGas.electricity: "/v1/electricity-meter-points/{mpn}/meters/{serial}/consumption/",
    ElectricOrGas.gas: "/v1/gas-meter-points/{mpn}/meters/{serial}/consumption/",
}


class Meter(BaseModel):
    name: str
    type: ElectricOrGas
    serial: str
    mpn: str


class OctopusConfig(BaseModel):
    api_key: str
    meters: List[Meter]
