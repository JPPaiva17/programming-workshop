import asyncio
import logging
import signal
from chat_producer import ChatProducer
from websocket_server import WebSocketServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")


async def main() -> None:
    chat_producer = ChatProducer("chat-messages")
    ws_server = WebSocketServer(chat_producer)
    await ws_server.start(host="0.0.0.0", port=8080)

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    await stop_event.wait()
    await ws_server.stop()
    chat_producer.close()


if __name__ == "__main__":
    asyncio.run(main())