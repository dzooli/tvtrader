from pydantic import BaseModel, Field


class TradingViewAlert(BaseModel):
    id: int = Field(description="Strategy ID", min=1, examples=[1, 2])
    name: str = Field(description="Strategy name", min_length=1, examples=["MYSTRAT"])
    symbol: str = Field(description="Symbol name", min_length=1, examples=["GBPUSD"])
    interval: int = Field(
        description="Strategy interval", ge=1, examples=[1, 5, 15, 60, 240]
    )
    direction: str = Field(
        description="Position direction",
        pattern=r"([bB][Uu][Yy]|[sS][eE][lL]+|[cC][lL][Oo][Ss][Ee]).*",
        examples=["buy", "sell", "close", "BUY", "SELL", "CLOSE"],
    )
    price: float = Field(
        description="The current price of the security",
        min=0.0,
        examples=[1.11221],
    )
    timestamp: str = Field(
        description="Timestamp of the alert in UTC time without milliseconds",
        min_length=19,
        examples=["2019-08-27T09:56:00Z"],
    )
