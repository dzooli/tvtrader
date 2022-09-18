from attrs import define, validators, field


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
            validators.min_len(1)
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
            validators.min_len(1)
        ]
    )
