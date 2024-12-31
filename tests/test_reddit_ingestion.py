import pytest
from reddit_ingestion import create_reddit_client


def test_create_reddit_client():
    client = create_reddit_client()
    assert client is not None
