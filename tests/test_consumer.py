from unittest.mock import patch, MagicMock
from ingestion import KafkaConsumerManager


@patch("ingestion.kafka_consumer.KafkaConsumer")
def test_create_consumer(mock_kafka_consumer):
    """
    Test the creation of a Kafka consumer.
    """
    # Mock KafkaConsumer instance
    mock_consumer_instance = MagicMock()
    mock_kafka_consumer.return_value = mock_consumer_instance

    # Initialize KafkaConsumerManager
    topic = "test_topic"
    consumer_manager = KafkaConsumerManager(topic)

    # Assert that the Kafka consumer instance is not None
    assert consumer_manager.consumer is not None, "Failed to create Kafka consumer instance."

    # Verify that KafkaConsumer was called with the correct arguments
    mock_kafka_consumer.assert_called_once_with(
        topic,
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="default_group",
        value_deserializer=MagicMock(),
    )

    # Close the consumer manager after the test
    consumer_manager.close()
