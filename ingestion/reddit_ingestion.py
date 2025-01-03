import praw
from ingestion.logger import logger
from dotenv import load_dotenv
import os

class RedditConfig:
    """
    Encapsulates Reddit API configuration.
    """
    load_dotenv()  # Load environment variables from a .env file if present

    CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_reddit_client_id")
    CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "your_reddit_client_secret")
    USER_AGENT = os.getenv("REDDIT_USER_AGENT", "your_user_agent")

    @staticmethod
    def validate():
        """
        Validates critical Reddit configurations.
        Raises:
            ValueError: If a required configuration is missing.
        """
        if not RedditConfig.CLIENT_ID or RedditConfig.CLIENT_ID == "your_reddit_client_id":
            raise ValueError("REDDIT_CLIENT_ID is not set or is using the default value!")
        if not RedditConfig.CLIENT_SECRET or RedditConfig.CLIENT_SECRET == "your_reddit_client_secret":
            raise ValueError("REDDIT_CLIENT_SECRET is not set or is using the default value!")
        if not RedditConfig.USER_AGENT or RedditConfig.USER_AGENT == "your_user_agent":
            raise ValueError("REDDIT_USER_AGENT is not set or is using the default value!")

# Validate configurations at runtime
RedditConfig.validate()


class RedditClient:
    """
    Manages interactions with the Reddit API.
    """
    def __init__(self):
        """
        Initializes the RedditClient using credentials from RedditConfig.
        """
        self.reddit = self._create_client()

    def _create_client(self):
        """
        Creates and returns a Reddit API client.
        """
        try:
            reddit = praw.Reddit(
                client_id=RedditConfig.CLIENT_ID,
                client_secret=RedditConfig.CLIENT_SECRET,
                user_agent=RedditConfig.USER_AGENT,
            )
            logger.info("Connected to Reddit API.")
            return reddit
        except Exception as e:
            logger.error("Failed to create Reddit client: %s", e)
            raise

    def get_subreddit(self, subreddit_name):
        """
        Retrieves a subreddit object.

        Args:
            subreddit_name (str): Name of the subreddit.

        Returns:
            Subreddit: The subreddit object.
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            logger.info("Retrieved subreddit: %s", subreddit_name)
            return subreddit
        except Exception as e:
            logger.error("Failed to retrieve subreddit '%s': %s", subreddit_name, e)
            raise
