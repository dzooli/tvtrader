from attrs import define, validators, field
from sanic_openapi import doc


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
            validators.in_(["BUY", "SELL", "buy", "sell"])
        ]
    )
    timestamp: str = field(
        validator=[
            validators.instance_of(str),
            validators.min_len(10)
        ]
    )


class TradingViewAlertSchema:
    stratId = doc.Integer(
        description="Strategy identifier", required=True)
    stratName = doc.String(
        description="Strategy name", required=True)
    symbol = doc.String(
        description="Symbol for the alert", required=True)
    interval = doc.Integer(
        description="Strategy operational timeframe, minimum value 1", required=True)
    direction = doc.String(
        choices=["BUY", "buy", "SELL", "sell"], description="Strategy direction", required=True)
    timestamp = doc.DateTime(
        description="Timestamp of the alert in UTC time without milliseconds", required=True)
