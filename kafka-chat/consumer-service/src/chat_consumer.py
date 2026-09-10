import logging
import asyncio

from kafka import KafkaConsumer

logger = logging.getLogger("chat_consumer")

TOPIC = "chat-messages"
BOOTSTRAP_SERVERS = "kafka:9092"
GROUP_ID = "chat-consumer-group"

async def consume_forever(broadcast_callback) -> None:
    """Consome mensagens do Kafka indefinidamente e as retransmite.
    broadcast_callback deve ser uma coroutine que recebe uma string
    (o texto da mensagem) e a envia para os clientes WebSocket
    conectados (equivalente a WebSocketServer.broadcast() no Java).
    """
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        value_deserializer=lambda value: value.decode("utf-8"),
    )

    loop = asyncio.get_running_loop()
    logger.info("Consumidor inscrito no topico '%s'", TOPIC)
    try:
        while True:
            records = await loop.run_in_executor(None, consumer.poll, 100)
            for _topic_partition, messages in records.items():
                for record in messages:
                    logger.info("Mensagem recebida: %s", record.value)
                    await broadcast_callback(record.value)
    finally:
        consumer.close()