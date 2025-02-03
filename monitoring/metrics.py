from prometheus_client import Counter, Histogram, Gauge

class MetricsCollector:
    def __init__(self):
        # Kafka metrics
        self.kafka_messages_total = Counter(
            'kafka_messages_total',
            'Total number of Kafka messages processed'
        )
        self.kafka_processing_time = Histogram(
            'kafka_processing_seconds',
            'Time spent processing Kafka messages'
        )

        # Reddit metrics
        self.reddit_api_calls = Counter(
            'reddit_api_calls_total',
            'Total number of Reddit API calls'
        )
        self.reddit_api_errors = Counter(
            'reddit_api_errors_total',
            'Total number of Reddit API errors'
        )

        # Snowflake metrics
        self.snowflake_write_latency = Histogram(
            'snowflake_write_seconds',
            'Time spent writing to Snowflake'
        )
        self.snowflake_active_connections = Gauge(
            'snowflake_active_connections',
            'Number of active Snowflake connections'
        )