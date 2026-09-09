import logging
from datetime import datetime
from kafka import KafkaProducer

logger = logging.getLogger("chat_producer")

KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"

class ChatProducer:
    """Produtor de mensagens de chat para um tópico Kafka."""

    def __init__(self, topic: str):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda value: value.encode("utf-8"),
        )
    
    def send_message(self, message: str) -> None:
        """Envia uma mensagem para o tópico, com data/hora na frente."""
        timestamped = f"{datetime.now()} ==> {message}"
        self.producer.send(self.topic, value=timestamped)
        self.producer.flush()
        logger.info("Mensagem publicada no tópico %s: %s", self.topic, timestamped)

    def close(self):
        """Fecha a conexão com o Kafka."""
        self.producer.close()