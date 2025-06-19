from kafka import KafkaProducer, KafkaConsumer
from config import config
from logger import logger
import threading

producer = KafkaProducer(bootstrap_servers=[config.KAFKA_BROKER], value_serializer=lambda v: v)


def kafka_produce(topic: str, data: bytes):
    producer.send(topic, data)
    producer.flush()
    logger.debug(f"Produced to {topic}: {len(data)} bytes")


def start_kafka_consumer(topic: str, callback):
    def run():
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[config.KAFKA_BROKER],
            auto_offset_reset="latest",
            enable_auto_commit=True,
            value_deserializer=lambda v: v,
        )
        logger.info(f"Kafka consumer listening on {topic}")
        for msg in consumer:
            callback(msg.value)

    threading.Thread(target=run, daemon=True).start()
