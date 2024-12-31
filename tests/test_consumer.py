import pytest
from kafka_consumer import create_consumer


def test_create_consumer():
    consumer = create_consumer("test_topic")
    assert consumer is not None
