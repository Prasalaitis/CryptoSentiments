import pytest
from kafka_producer import create_producer, send_message


def test_create_producer():
    producer = create_producer()
    assert producer is not None


def test_send_message():
    producer = create_producer()
    send_message(producer, "test_topic", {"key": "value"})
