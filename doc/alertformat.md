# TradingView alert settings

## General rules

- Do not add blocking pop-up window
- Do not add disturbing actions
- Use the strategy.comment as "BUY" or "SELL" only
- Keep the Alerts panel open (the page script is based on this panel)

## Alert message content

```json
{
    "id":1,
    "name":"WINNER",
    "symbol": "{{exchange}}:{{ticker}}",
    "price": "{{close}}",
    "interval":{{interval}},
    "direction":"{{strategy.order.comment}}",
    "timestamp": "{{timenow}}"
}
```

## Screenshot

![alert image](./alert_setup.PNG)
