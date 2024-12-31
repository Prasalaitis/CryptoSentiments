import unittest
from unittest.mock import patch, MagicMock
from ingestion.kafka_setup import create_topics

class TestKafkaSetup(unittest.TestCase):
    @patch("ingestion.kafka_setup.KafkaAdminClient")
    def test_create_topics(self, mock_admin_client):
        # Mock KafkaAdminClient
        mock_admin_instance = MagicMock()
        mock_admin_client.return_value = mock_admin_instance

        # Define test topics
        test_topics = ["test_topic1", "test_topic2"]

        # Call create_topics
        create_topics(test_topics)

        # Check that KafkaAdminClient was initialized
        mock_admin_client.assert_called_once_with(
            bootstrap_servers="localhost:9092",
            client_id="admin"
        )

        # Check that create_topics was called with the correct parameters
        mock_admin_instance.create_topics.assert_called_once()
        created_topics = mock_admin_instance.create_topics.call_args[1]["new_topics"]
        self.assertEqual(len(created_topics), len(test_topics))
        self.assertEqual(created_topics[0].name, "test_topic1")
        self.assertEqual(created_topics[1].name, "test_topic2")

if __name__ == "__main__":
    unittest.main()
