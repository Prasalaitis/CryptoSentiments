import os
import praw
from ingestion.kafka_producer import create_producer, send_message
from ingestion.logger import logger
from ingestion.config import KAFKA_TOPICS
from dotenv import load_dotenv


# Load Reddit API credentials from environment variables
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_reddit_client_id")
REDDIT_CLIENT_SECRET = os.getenv(
    "REDDIT_CLIENT_SECRET", "your_reddit_client_secret"
)
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "your_user_agent")

load_dotenv()
# Access variables
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")


def create_reddit_client():
    """
    Creates and returns a Reddit API client.
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
        )
        logger.info("Connected to Reddit API.")
        return reddit
    except Exception as e:
        logger.error("Failed to create Reddit client: %s", e)
        raise


def stream_subreddit(subreddit_name, producer, topic):
    """
    Streams submissions from a subreddit and sends them to Kafka.

    Args:
        subreddit_name (str): Name of the subreddit to stream.
        producer: Kafka producer instance.
        topic (str): Kafka topic to send the messages to.
    """
    reddit = create_reddit_client()
    subreddit = reddit.subreddit(subreddit_name)

    try:
        for post in subreddit.stream.submissions(skip_existing=True):
            message = {
                "id": post.id,
                "title": post.title,
                "selftext": post.selftext,
                "created_utc": post.created_utc,
            }
            try:
                send_message(producer, topic, message)
                logger.info("Message sent to Kafka: %s", message)
            except Exception as e:
                logger.error("Failed to send message to Kafka: %s", e)
                # Retry logic could be added here
    except Exception as e:
        logger.error("Error while streaming subreddit data: %s", e)
        # Add retry logic or exit gracefully


if __name__ == "__main__":
    producer = create_producer()
    try:
        stream_subreddit(
            subreddit_name="cryptocurrency",
            producer=producer,
            topic=KAFKA_TOPICS[0],
        )
    finally:
        producer.close()
