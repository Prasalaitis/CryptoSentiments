import pytest
from unittest.mock import patch, Mock
from ingestion.binance_api import fetch_binance_coins

@patch("ingestion.binance_api.requests.get")
def test_fetch_binance_coins_success(mock_get):
    # Mock API response
    mock_response = Mock()
    mock_response.json.return_value = {
        "symbols": [
            {"symbol": "BTCUSDT"},
            {"symbol": "ETHUSDT"},
            {"symbol": "BNBUSDT"}
        ]
    }
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the function
    symbols = fetch_binance_coins()

    # Assertions
    assert len(symbols) == 3
    assert symbols == ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    mock_get.assert_called_once()

@patch("ingestion.binance_api.requests.get")
def test_fetch_binance_coins_retry(mock_get):
    # Mock API response to simulate failure
    mock_get.side_effect = [
        Mock(side_effect=Exception("Timeout")),
        Mock(side_effect=Exception("Server Error")),
        Mock(return_value=Mock(status_code=200, json=lambda: {"symbols": []}))
    ]

    # Call the function
    symbols = fetch_binance_coins()

    # Assertions
    assert symbols == []
    assert mock_get.call_count == 3

@patch("ingestion.binance_api.requests.get")
def test_fetch_binance_coins_empty_response(mock_get):
    # Mock API response with no symbols
    mock_response = Mock()
    mock_response.json.return_value = {"symbols": []}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the function
    symbols = fetch_binance_coins()

    # Assertions
    assert symbols == []
    mock_get.assert_called_once()

@patch("ingestion.binance_api.requests.get")
def test_fetch_binance_coins_invalid_format(mock_get):
    # Mock API response with invalid JSON structure
    mock_response = Mock()
    mock_response.json.return_value = {}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Call the function
    symbols = fetch_binance_coins()

    # Assertions
    assert symbols == []
    mock_get.assert_called_once()

@patch("ingestion.binance_api.requests.get")
def test_fetch_binance_coins_api_failure(mock_get):
    # Mock API failure with HTTP error
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_get.return_value = mock_response

    # Call the function
    symbols = fetch_binance_coins()

    # Assertions
    assert symbols == []
    mock_get.assert_called_once()