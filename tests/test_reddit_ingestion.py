import pytest
from unittest.mock import patch, Mock
from ingestion.reddit_ingestion import RedditClient, RedditConfig

@patch("ingestion.reddit_ingestion.praw.Reddit")
def test_reddit_client_initialization(mock_praw_reddit):
    # Mock Reddit instance
    mock_reddit_instance = Mock()
    mock_praw_reddit.return_value = mock_reddit_instance

    client = RedditClient()

    mock_praw_reddit.assert_called_once_with(
        client_id=RedditConfig.CLIENT_ID,
        client_secret=RedditConfig.CLIENT_SECRET,
        user_agent=RedditConfig.USER_AGENT
    )
    assert client.reddit == mock_reddit_instance

@patch("ingestion.reddit_ingestion.praw.Reddit")
def test_fetch_subreddit_posts(mock_praw_reddit):
    # Mock subreddit and posts
    mock_post1 = Mock(title="Post 1")
    mock_post2 = Mock(title="Post 2")
    mock_subreddit = Mock()
    mock_subreddit.new.return_value = [mock_post1, mock_post2]

    mock_reddit_instance = Mock()
    mock_reddit_instance.subreddit.return_value = mock_subreddit
    mock_praw_reddit.return_value = mock_reddit_instance

    client = RedditClient()
    posts = list(client.fetch_subreddit_posts("test_subreddit", limit=2))

    mock_reddit_instance.subreddit.assert_called_once_with("test_subreddit")
    mock_subreddit.new.assert_called_once_with(limit=2)

    assert len(posts) == 2
    assert posts[0].title == "Post 1"
    assert posts[1].title == "Post 2"

@patch("ingestion.reddit_ingestion.praw.Reddit")
def test_fetch_subreddit_posts_invalid_subreddit(mock_praw_reddit):
    # Mock invalid subreddit access
    mock_reddit_instance = Mock()
    mock_reddit_instance.subreddit.side_effect = Exception("Invalid subreddit")
    mock_praw_reddit.return_value = mock_reddit_instance

    client = RedditClient()

    with pytest.raises(Exception, match="Invalid subreddit"):
        list(client.fetch_subreddit_posts("invalid_subreddit"))

    mock_reddit_instance.subreddit.assert_called_once_with("invalid_subreddit")
