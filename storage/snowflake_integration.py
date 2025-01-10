import snowflake.connector
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class SnowflakeIntegration:
    def __init__(self):
        """
        Initialize the Snowflake connection using environment variables.
        """
        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
                role=os.getenv("SNOWFLAKE_ROLE")
            )
            logging.info("Snowflake connection established.")
        except Exception as e:
            logging.error("Failed to connect to Snowflake: %s", e)
            raise

    def create_table(self):
        """
        Create the sentiment_analysis_results table in Snowflake.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sentiment_analysis_results (
                    id STRING,
                    subreddit STRING,
                    title STRING,
                    body STRING,
                    sentiment STRING,
                    timestamp TIMESTAMP
                )
                """
            )
            logging.info("Table sentiment_analysis_results created or already exists.")
        except Exception as e:
            logging.error("Failed to create table in Snowflake: %s", e)
        finally:
            cursor.close()

    def write_data(self, data):
        """
        Write processed data into Snowflake.

        Args:
            data (list of dict): Data to insert into Snowflake.
        """
        try:
            cursor = self.conn.cursor()
            for row in data:
                cursor.execute(
                    """
                    INSERT INTO sentiment_analysis_results (id, subreddit, title, body, sentiment, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (row['id'], row['subreddit'], row['title'], row['body'], row['sentiment'], row['timestamp'])
                )
            logging.info("Data successfully written to Snowflake.")
        except Exception as e:
            logging.error("Failed to write data to Snowflake: %s", e)
        finally:
            cursor.close()

    def close(self):
        """
        Close the Snowflake connection.
        """
        try:
            self.conn.close()
            logging.info("Snowflake connection closed.")
        except Exception as e:
            logging.error("Failed to close Snowflake connection: %s", e)

if __name__ == "__main__":
    # Example usage
    snowflake_integration = SnowflakeIntegration()
    try:
        snowflake_integration.create_table()
        # Example data
        example_data = [
            {
                "id": "1",
                "subreddit": "cryptocurrency",
                "title": "Bitcoin hits $30k",
                "body": "Bitcoin has reached $30,000 today!",
                "sentiment": "positive",
                "timestamp": "2025-01-10 12:00:00"
            }
        ]
        snowflake_integration.write_data(example_data)
    except Exception as e:
        logging.error("Error in Snowflake operations: %s", e)
    finally:
        snowflake_integration.close()
