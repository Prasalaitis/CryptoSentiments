import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from a .env file if it exists
load_dotenv()

class ConfigBase:
    """
    Base class for configurations, providing validation and utility methods.
    """

    @staticmethod
    def validate_env_variable(var_name: str, default: Any = None) -> Any:
        """
        Validates that an environment variable is set. Uses a default if provided.

        Args:
            var_name (str): Name of the environment variable.
            default (Any): Default value if the variable is not set.

        Returns:
            Any: The value of the environment variable or the default value.

        Raises:
            ValueError: If the variable is not set and no default is provided.
        """
        value = os.getenv(var_name, default)
        if value is None:
            raise ValueError(f"Environment variable {var_name} is not set and no default is provided!")
        return value

class KafkaConfig(ConfigBase):
    """
    Encapsulates Kafka configurations for better reusability.
    """
    # Kafka Connection
    BOOTSTRAP_SERVERS: str = ConfigBase.validate_env_variable("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    PARTITIONS: int = int(ConfigBase.validate_env_variable("KAFKA_PARTITIONS", 3))
    REPLICATION_FACTOR: int = int(ConfigBase.validate_env_variable("KAFKA_REPLICATION_FACTOR", 2))
    GROUP_ID: str = ConfigBase.validate_env_variable("KAFKA_GROUP_ID", "default-consumer-group")

    # Kafka Topics
    TOPICS: Dict[str, str] = {
        "main": ConfigBase.validate_env_variable("KAFKA_MAIN_TOPIC", "cryptocurrency_events"),
        "results": ConfigBase.validate_env_variable("KAFKA_RESULTS_TOPIC", "sentiment_analysis_results"),
        "dlq": ConfigBase.validate_env_variable("KAFKA_DLQ_TOPIC", "dead_letter_queue"),
    }

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        """
        Returns the Kafka configuration as a dictionary for easier debugging or logging.

        Returns:
            Dict[str, Any]: Kafka configurations.
        """
        return {
            "BOOTSTRAP_SERVERS": cls.BOOTSTRAP_SERVERS,
            "PARTITIONS": cls.PARTITIONS,
            "REPLICATION_FACTOR": cls.REPLICATION_FACTOR,
            "GROUP_ID": cls.GROUP_ID,
            "TOPICS": cls.TOPICS,
        }

if __name__ == "__main__":
    # Print configurations for debugging purposes
    kafka_config = KafkaConfig.as_dict()
    print("Kafka Configurations:", kafka_config)