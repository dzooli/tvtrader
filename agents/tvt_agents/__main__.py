import logging
import wsaccel


from .distributor import RabbitDistributor

print("agents package main")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, force=True)
    wsaccel.patch_ws4py()
    try:
        ws = RabbitDistributor(
            "wss://api.gemini.com/v1/marketdata/BTCUSD", protocols=["http-only", "chat"]
        )
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
