import pytest
from unittest.mock import patch, Mock
from kafka import KafkaProducer
from ingestion.kafka_producer import KafkaProducerManager
from ingestion.config import KafkaConfig

@patch("ingestion.kafka_producer.KafkaProducer")
def test_kafka_producer_send_success(mock_kafka_producer):
    # Mock KafkaProducer behavior
    mock_producer_instance = Mock()
    mock_kafka_producer.return_value = mock_producer_instance

    producer_manager = KafkaProducerManager()
    sample_message = {"key": "value"}

    producer_manager.send_message(topic_key="main", message=sample_message)
    producer_manager.close()

    mock_producer_instance.send.assert_called_once_with(
        KafkaConfig.TOPICS["main"], value=sample_message
    )
    mock_producer_instance.close.assert_called_once()

@patch("ingestion.kafka_producer.KafkaProducer")
def test_kafka_producer_retry_logic(mock_kafka_producer):
    # Mock KafkaProducer to simulate failure and retry
    mock_producer_instance = Mock()
    mock_producer_instance.send.side_effect = [Exception("Send failure"), None]
    mock_kafka_producer.return_value = mock_producer_instance

    producer_manager = KafkaProducerManager()
    sample_message = {"key": "value"}

    producer_manager.send_message(topic_key="main", message=sample_message, retries=1)
    producer_manager.close()

    assert mock_producer_instance.send.call_count == 2
    mock_producer_instance.close.assert_called_once()

@patch("ingestion.kafka_producer.KafkaProducer")
def test_kafka_producer_invalid_topic(mock_kafka_producer):
    # Mock KafkaProducer
    mock_producer_instance = Mock()
    mock_kafka_producer.return_value = mock_producer_instance

    producer_manager = KafkaProducerManager()

    with pytest.raises(ValueError, match="Topic 'invalid_topic' not found in KafkaConfig.TOPICS"):
        producer_manager.send_message(topic_key="invalid_topic", message={"key": "value"})

    producer_manager.close()
    mock_producer_instance.close.assert_called_once()