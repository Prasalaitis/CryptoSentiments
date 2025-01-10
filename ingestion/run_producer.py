from kafka_producer import KafkaProducerManager

# Initialize the Kafka producer
producer_manager = KafkaProducerManager()

try:
    # Define a test message
    sample_message = {"event": "price_update", "coin": "BTC", "price": "30000"}

    # Send the message to the 'main' topic
    producer_manager.send_message(topic_key="main", message=sample_message)
    print("Message sent successfully!")
except Exception as e:
    print(f"Producer error: {e}")
finally:
    # Close the producer
    producer_manager.close()
