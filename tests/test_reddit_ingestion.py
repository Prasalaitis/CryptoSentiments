from ingestion import RedditClient

def test_create_reddit_client():
    """
    Test the creation of a Reddit client.
    """
    # Create an instance of RedditClient
    reddit_client = RedditClient()

    # Assert that the Reddit client instance is not None
    assert reddit_client.reddit is not None, "Failed to create Reddit client instance."

    # Optionally, check a simple functionality like accessing a subreddit
    subreddit = reddit_client.get_subreddit("test")
    assert subreddit is not None, "Failed to access subreddit using Reddit client."
