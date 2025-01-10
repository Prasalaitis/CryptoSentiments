from kafka_consumer import KafkaConsumerManager

# Define a test handler to process messages
def test_handler(message):
    print(f"Message processed: {message}")

# Initialize the Kafka consumer
consumer_manager = KafkaConsumerManager(topic_key="main", message_handler=test_handler)

try:
    print("Starting consumer...")
    # Consume messages (this will block until interrupted)
    consumer_manager.consume_messages()
except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    # Close the consumer
    consumer_manager.close()
