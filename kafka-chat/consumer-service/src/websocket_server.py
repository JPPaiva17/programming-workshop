import logging
import websockets

from websockets.server import WebSocketServerProtocol

logger = logging.getLogger("websocket_server")
ENDPOINT_PATH = "/chat/ws"

class WebSocketServer:
    """Servidor WebSocket assíncrono que apenas retransmite mensagens."""
    def __init__(self):
        self.connections: set[WebSocketServerProtocol] = set()
        self._server = None

    async def _handler(self, websocket: WebSocketServerProtocol) -> None:
        path = getattr(websocket, "path", ENDPOINT_PATH)
        if path not in (ENDPOINT_PATH, "/"):
            await websocket.close(code=1008, reason="endpoint invalido")
            return
        self.connections.add(websocket)
        try:
            async for message in websocket:
                if isinstance(message, bytes):
                    message = message.decode("utf-8")
                await self.broadcast(message)
        except websockets.ConnectionClosed:
            pass
        finally:
            self.connections.discard(websocket)
        
    async def broadcast(self, message: str) -> None:
        """Envia a mensagem, sem alteracoes, para todos os clientes."""
        stale = set()
        for client in self.connections:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                stale.add(client)
                self.connections -= stale
        
    async def start(self, host: str = "0.0.0.0", port: int = 8080) -> None:
        """Inicia o servidor WebSocket"""
        self._server = await websockets.serve(self._handler, host, port)
        logger.info("Servidor WebSocket do consumidor ouvindo em %s:%d%s", host, port, ENDPOINT_PATH)
    
    async def stop(self) -> None:
        """Encerra o servidor"""
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()