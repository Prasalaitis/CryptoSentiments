import os
import logging
import snowflake.connector
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_env_vars(vars_to_check: List[str]) -> bool:
    """
    Validates that the required environment variables are set.

    Args:
        vars_to_check (List[str]): List of environment variable names.

    Returns:
        bool: True if all variables are set, False otherwise.
    """
    for var in vars_to_check:
        if not os.getenv(var):
            logging.error("Missing required environment variable: %s", var)
            return False
    return True


def insert_into_snowflake(data: List[Dict[str, Any]]):
    """
    Inserts data into the Snowflake `reddit_data` table.

    Args:
        data (List[Dict[str, Any]]): A list of dictionaries containing column-value pairs.
    """
    # Validate environment variables
    required_vars = [
        "SNOWFLAKE_USER",
        "SNOWFLAKE_PASSWORD",
        "SNOWFLAKE_ACCOUNT",
        "SNOWFLAKE_DATABASE",
        "SNOWFLAKE_SCHEMA",
        "SNOWFLAKE_TABLE",
    ]
    if not validate_env_vars(required_vars):
        logging.error(
            "One or more required environment variables are missing."
        )
        return

    # Load credentials from environment variables
    snowflake_user = os.getenv("SNOWFLAKE_USER")
    snowflake_password = os.getenv("SNOWFLAKE_PASSWORD")
    snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
    snowflake_database = os.getenv("SNOWFLAKE_DATABASE")
    snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA")
    snowflake_table = os.getenv("SNOWFLAKE_TABLE")

    # Establish connection
    try:
        logging.info("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account,
            database=snowflake_database,
            schema=snowflake_schema,
        )
        logging.info("Connected to Snowflake.")

        # Create a cursor
        cur = conn.cursor()

        # Build insert query dynamically
        columns = data[0].keys()
        query = f"INSERT INTO {snowflake_table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

        # Insert data in batches
        logging.info("Inserting data into Snowflake...")
        batch_size = 100  # Adjust batch size as needed
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            values = [tuple(row.values()) for row in batch]
            cur.executemany(query, values)

        # Commit changes
        conn.commit()
        logging.info("Data inserted successfully.")

    except snowflake.connector.Error as e:
        logging.error("Snowflake error: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)
    finally:
        # Ensure resources are closed
        try:
            if cur:
                cur.close()
            if conn:
                conn.close()
            logging.info("Snowflake connection closed.")
        except NameError:
            logging.warning("Cursor or connection was not initialized.")


if __name__ == "__main__":
    # Example data to insert
    example_data = [
        {
            "column1": "value1",
            "column2": "value2",
            "column3": "value3",
            "column4": "value4",
        },
        {
            "column1": "value5",
            "column2": "value6",
            "column3": "value7",
            "column4": "value8",
        },
    ]
    insert_into_snowflake(example_data)
