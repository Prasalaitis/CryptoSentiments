from ingestion import KafkaProducerManager

def test_create_producer():
    """
    Test the creation of a Kafka producer.
    """
    # Create an instance of KafkaProducerManager
    producer_manager = KafkaProducerManager()

    # Assert that the producer instance is not None
    assert producer_manager.producer is not None, "Failed to create Kafka producer instance."

    # Close the producer after the test
    producer_manager.close()


def test_send_message():
    """
    Test sending a message using the Kafka producer.
    """
    # Create an instance of KafkaProducerManager
    producer_manager = KafkaProducerManager()

    # Send a test message to a Kafka topic
    try:
        producer_manager.send_message("test_topic", {"key": "value"})
    except Exception as e:
        assert False, f"Failed to send message: {e}"

    # Close the producer after the test
    producer_manager.close()
