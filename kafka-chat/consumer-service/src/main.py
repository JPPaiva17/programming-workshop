import asyncio
import logging

from chat_consumer import consume_forever
from websocket_server import WebSocketServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

async def main() -> None:
    ws_server = WebSocketServer()
    await ws_server.start(host="0.0.0.0", port=8080)
    await consume_forever(ws_server.broadcast)

if __name__ == "__main__":
    asyncio.run(main())