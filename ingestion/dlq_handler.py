from ingestion.kafka_producer import KafkaProducerManager
from ingestion.logger import logger

def send_to_dlq(producer_manager, topic, message):
    """
    Sends a failed message to the Dead Letter Queue (DLQ).

    Args:
        producer_manager (KafkaProducerManager): Kafka producer manager instance.
        topic (str): Kafka topic name for DLQ.
        message (dict): The message to send to DLQ.
    """
    try:
        producer_manager.send_message(topic, message)
        logger.info("Message sent to DLQ: %s", message)
    except Exception as e:
        logger.error("Failed to send message to DLQ: %s", e)
