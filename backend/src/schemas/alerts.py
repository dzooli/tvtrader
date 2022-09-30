from attrs import define, validators, field
from sanic_ext import openapi


@define
class TradingViewAlert:
    stratId: int = field(
        validator=[
            validators.instance_of(int),
            validators.ge(0)
        ]
    )
    stratName: str = field(
        validator=[
            validators.instance_of(str),
        ]
    )
    symbol: str = field(
        validator=[
            validators.instance_of(str),
            validators.min_len(1)
        ]
    )
    interval: int = field(
        validator=[
            validators.instance_of(int),
            validators.ge(1)
        ]
    )
    direction: str = field(
        validator=[
            validators.instance_of(str),
            validators.in_(["BUY", "SELL"])
        ]
    )
    timestamp: str = field(
        validator=[
            validators.instance_of(str),
            validators.min_len(10)
        ]
    )


class TradingViewAlertSchema:
    stratId = openapi.Integer(
        description="Strategy identifier", required=True, example=1)
    stratName = openapi.String(
        description="Strategy name", required=True, example="EMARSI")
    symbol = openapi.String(
        description="Symbol for the alert", required=True, example="GBPUSD")
    interval = openapi.Integer(
        description="Strategy operational timeframe", required=True, example=15)
    #direction = list(["BUY", "SELL"])
    direction = openapi.String(description="Strategy direction",
                               oneOf=["BUY", "SELL"], required=True)
    timestamp = openapi.DateTime(
        description="Timestamp of the alert in UTC time", required=True, example="2022-09-30T16:22:02Z")
