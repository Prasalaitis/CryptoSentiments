import unittest
from unittest.mock import patch, MagicMock
from ingestion.kafka_setup import create_topics


class TestKafkaSetup(unittest.TestCase):
    @patch("ingestion.kafka_setup.KafkaAdminClient")
    def test_create_topics(self, mock_admin_client):
        """
        Test the create_topics function with mocked KafkaAdminClient.
        """
        # Mock KafkaAdminClient
        mock_admin_instance = MagicMock()
        mock_admin_client.return_value = mock_admin_instance

        # Define test topics
        test_topics = ["test_topic1", "test_topic2"]

        # Call create_topics
        create_topics(test_topics)

        # Verify KafkaAdminClient was initialized
        mock_admin_client.assert_called_once_with(
            bootstrap_servers="localhost:9092", client_id="admin"
        )

        # Verify create_topics was called with the correct parameters
        mock_admin_instance.create_topics.assert_called_once()
        created_topics = mock_admin_instance.create_topics.call_args[1]["new_topics"]

        # Assert the number of topics matches
        self.assertEqual(len(created_topics), len(test_topics))

        # Assert topic names match the test topics
        self.assertEqual(created_topics[0].name, "test_topic1")
        self.assertEqual(created_topics[1].name, "test_topic2")

    @patch("ingestion.kafka_setup.KafkaAdminClient")
    def test_create_topics_existing_topics(self, mock_admin_client):
        """
        Test create_topics when topics already exist.
        """
        # Mock KafkaAdminClient
        mock_admin_instance = MagicMock()
        mock_admin_instance.list_topics.return_value = ["test_topic1"]
        mock_admin_client.return_value = mock_admin_instance

        # Define test topics
        test_topics = ["test_topic1", "test_topic2"]

        # Call create_topics
        create_topics(test_topics)

        # Verify KafkaAdminClient was initialized
        mock_admin_client.assert_called_once_with(
            bootstrap_servers="localhost:9092", client_id="admin"
        )

        # Verify create_topics was called only for non-existing topics
        mock_admin_instance.create_topics.assert_called_once()
        created_topics = mock_admin_instance.create_topics.call_args[1]["new_topics"]

        # Assert only the new topic is created
        self.assertEqual(len(created_topics), 1)
        self.assertEqual(created_topics[0].name, "test_topic2")


if __name__ == "__main__":
    unittest.main()
