import praw
from ingestion.logger import logger
from dotenv import load_dotenv
import os
from typing import Any

class RedditConfig:
    """
    Encapsulates Reddit API configuration and validation.
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
            raise ValueError("REDDIT_CLIENT_ID is not set or is using the default placeholder value.")
        if not RedditConfig.CLIENT_SECRET or RedditConfig.CLIENT_SECRET == "your_reddit_client_secret":
            raise ValueError("REDDIT_CLIENT_SECRET is not set or is using the default placeholder value.")
        if not RedditConfig.USER_AGENT or RedditConfig.USER_AGENT == "your_user_agent":
            raise ValueError("REDDIT_USER_AGENT is not set or is using the default placeholder value.")

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

    def _create_client(self) -> praw.Reddit:
        """
        Creates and returns a Reddit API client.

        Returns:
            praw.Reddit: Configured Reddit client instance.
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

    def fetch_subreddit_posts(self, subreddit_name: str, limit: int = 100) -> Any:
        """
        Fetches posts from a subreddit.

        Args:
            subreddit_name (str): Name of the subreddit.
            limit (int): Number of posts to fetch (default: 100).

        Returns:
            Any: Generator of subreddit posts.

        Raises:
            ValueError: If subreddit_name is empty.
        """
        if not subreddit_name:
            raise ValueError("Subreddit name cannot be empty.")

        try:
            logger.info("Fetching posts from subreddit: %s", subreddit_name)
            subreddit = self.reddit.subreddit(subreddit_name)
            return subreddit.new(limit=limit)
        except Exception as e:
            logger.error("Failed to fetch posts from subreddit '%s': %s", subreddit_name, e)
            raise


if __name__ == "__main__":
    try:
        client = RedditClient()
        subreddit_name = "cryptocurrency"
        posts = client.fetch_subreddit_posts(subreddit_name, limit=10)

        for post in posts:
            logger.info("Post Title: %s", post.title)
    except Exception as e:
        logger.error("Error in Reddit ingestion: %s", e)