import praw
from ingestion.logger import logger
from dotenv import load_dotenv
import os

class RedditClient:
    def __init__(self):
        """
        Initializes the RedditClient by loading credentials from environment variables.
        """
        load_dotenv()
        self.client_id = os.getenv("REDDIT_CLIENT_ID", "your_reddit_client_id")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET", "your_reddit_client_secret")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "your_user_agent")
        self.reddit = self._create_client()

    def _create_client(self):
        """
        Creates and returns a Reddit API client.
        """
        try:
            reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
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
        return self.reddit.subreddit(subreddit_name)
