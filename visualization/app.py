import streamlit as st
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# App title and description
st.title("Meme Coin Radar")
st.subheader("Track sentiment trends of meme coins in real-time!")

# Environment variables for dynamic configuration
DATA_SOURCE = os.getenv(
    "DATA_SOURCE", "processed_data.csv"
)  # Default to local CSV file
DEFAULT_COLUMN = os.getenv(
    "DEFAULT_COLUMN", "sentiment"
)  # Default column to display


def load_data(source: str) -> pd.DataFrame:
    """
    Load data from the specified source.

    Args:
        source (str): Path to the data file or data source.

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    try:
        if source.startswith("s3://"):
            import boto3
            from io import StringIO

            # Parse S3 details
            bucket, key = source.replace("s3://", "").split("/", 1)
            s3 = boto3.client("s3")
            obj = s3.get_object(Bucket=bucket, Key=key)
            df = pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))
        else:
            df = pd.read_csv(source)
        logging.info("Data loaded successfully from %s", source)
        return df
    except Exception as e:
        logging.error("Failed to load data: %s", e)
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()


def validate_data(df: pd.DataFrame) -> bool:
    """
    Validate the structure of the loaded DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    required_columns = [
        "sentiment",
        "timestamp",
    ]  # Adjust based on your dataset
    if df.empty:
        st.error("The loaded dataset is empty.")
        return False
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return False
    return True


def main():
    # Load data
    data = load_data(DATA_SOURCE)

    # Validate data
    if not validate_data(data):
        return

    # Display a preview of the data
    st.write("Here's a preview of the dataset:")
    st.dataframe(data.head())

    # Allow users to select the column to visualize
    st.write("Select a column to visualize its trend:")
    columns = data.columns.tolist()
    default_index = (
        columns.index(DEFAULT_COLUMN) if DEFAULT_COLUMN in columns else 0
    )
    selected_column = st.selectbox(
        "Choose a column", columns, index=default_index
    )

    # Allow users to filter by date range
    st.write("Filter data by date range:")
    min_date, max_date = pd.to_datetime(
        data["timestamp"].min()
    ), pd.to_datetime(data["timestamp"].max())
    date_range = st.date_input("Select date range", [min_date, max_date])
    if len(date_range) == 2:
        start_date, end_date = date_range
        data = data[
            (pd.to_datetime(data["timestamp"]) >= pd.to_datetime(start_date))
            & (pd.to_datetime(data["timestamp"]) <= pd.to_datetime(end_date))
        ]

    # Display the line chart for the selected column
    st.line_chart(data[selected_column])


if __name__ == "__main__":
    main()
