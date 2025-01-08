import pytest
from unittest.mock import patch, Mock
from kafka.admin import KafkaAdminClient
from kafka.errors import TopicAlreadyExistsError
from ingestion.kafka_setup import KafkaTopicManager
from ingestion.config import KafkaConfig

@patch("ingestion.kafka_setup.KafkaAdminClient")
def test_list_existing_topics(mock_kafka_admin_client):
    # Mock KafkaAdminClient behavior
    mock_admin_instance = Mock()
    mock_admin_instance.list_topics.return_value = ["topic1", "topic2", "topic3"]
    mock_kafka_admin_client.return_value = mock_admin_instance

    topic_manager = KafkaTopicManager()
    topics = topic_manager.list_existing_topics()
    topic_manager.close()

    assert topics == ["topic1", "topic2", "topic3"]
    mock_admin_instance.list_topics.assert_called_once()

@patch("ingestion.kafka_setup.KafkaAdminClient")
def test_create_new_topics(mock_kafka_admin_client):
    # Mock KafkaAdminClient behavior
    mock_admin_instance = Mock()
    mock_admin_instance.list_topics.return_value = ["existing_topic"]
    mock_kafka_admin_client.return_value = mock_admin_instance

    topic_manager = KafkaTopicManager()
    new_topics = topic_manager.create_topics(["new_topic", "existing_topic"])
    topic_manager.close()

    assert new_topics == ["new_topic"]
    mock_admin_instance.create_topics.assert_called_once()

@patch("ingestion.kafka_setup.KafkaAdminClient")
def test_create_existing_topic(mock_kafka_admin_client):
    # Mock KafkaAdminClient behavior
    mock_admin_instance = Mock()
    mock_admin_instance.list_topics.return_value = ["existing_topic"]
    mock_admin_instance.create_topics.side_effect = TopicAlreadyExistsError("Topic already exists")
    mock_kafka_admin_client.return_value = mock_admin_instance

    topic_manager = KafkaTopicManager()
    new_topics = topic_manager.create_topics(["existing_topic"])
    topic_manager.close()

    assert new_topics == []
    mock_admin_instance.create_topics.assert_called_once()

@patch("ingestion.kafka_setup.KafkaAdminClient")
def test_kafka_admin_client_close(mock_kafka_admin_client):
    # Mock KafkaAdminClient behavior
    mock_admin_instance = Mock()
    mock_kafka_admin_client.return_value = mock_admin_instance

    topic_manager = KafkaTopicManager()
    topic_manager.close()

    mock_admin_instance.close.assert_called_once()