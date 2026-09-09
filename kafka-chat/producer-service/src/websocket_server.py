import logging
from datetime import datetime
import websockets
from websockets.server import WebSocketServerProtocol

logger = logging.getLogger("websocket_server")
ENDPOINT_PATH = "/chat/ws"


class WebSocketServer:
    """Servidor WebSocket assíncrono que republica mensagens no Kafka."""
    def __init__(self, chat_producer):
        self.chat_producer = chat_producer
        self.connections: set[WebSocketServerProtocol] = set()
        self._server = None

    async def _handler(self, websocket: WebSocketServerProtocol) -> None:
        """Chamada uma vez por conexão de cliente (equivale a @OnOpen)."""
        path = getattr(websocket, "path", ENDPOINT_PATH)
        if path not in (ENDPOINT_PATH, "/"):
            await websocket.close(code=1008, reason="endpoint invalido")
            return

        self.connections.add(websocket)
        logger.info("Cliente conectado. Total de conexoes: %d", len(self.connections))
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    message = message.decode("utf-8")
                self.chat_producer.send_message(message)
                await self.broadcast(message)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.connections.discard(websocket)
            logger.info("Cliente desconectado. Total de conexoes: %d", len(self.connections))

    async def broadcast(self, message: str) -> None:
        """Envia a mensagem para todos os clientes conectados."""
        text = f"{datetime.now()} --> {message}"
        stale = set()
        for client in self.connections:
            try:
                await client.send(text)
            except websockets.ConnectionClosed:
                stale.add(client)
                self.connections -= stale
    
    async def start    (self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Inicia o servidor WebSocket (equivale a Server.start() no Java)."""
        self._server = await websockets.serve(self._handler, host, port)
        logger.info("Servidor WebSocket do produtor ouvindo em %s:%d%s", host, port, ENDPOINT_PATH)
 
    async def stop(self) -> None:
        """Encerra o servidor (equivale a Server.stop() no Java)."""
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()