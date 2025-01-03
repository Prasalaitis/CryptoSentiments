import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from kafka import KafkaConsumer
from ingestion.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPICS

class SentimentDashboard:
    def __init__(self):
        """
        Initializes the dashboard with default configuration.
        """
        self.consumer_cache = {}

    def get_kafka_consumer(self, topic):
        """
        Creates or retrieves a cached Kafka consumer for a given topic.

        Args:
            topic (str): The Kafka topic to consume messages from.

        Returns:
            KafkaConsumer: A Kafka consumer instance.
        """
        if topic not in self.consumer_cache:
            self.consumer_cache[topic] = KafkaConsumer(
                topic,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset="latest",
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
        return self.consumer_cache[topic]

    def fetch_data(self, consumer, max_messages=100):
        """
        Fetches data from a Kafka topic.

        Args:
            consumer (KafkaConsumer): The Kafka consumer instance.
            max_messages (int): The maximum number of messages to fetch.

        Returns:
            pd.DataFrame: A DataFrame containing the messages.
        """
        data = []
        for message in consumer:
            data.append(message.value)
            if len(data) >= max_messages:
                break
        return pd.DataFrame(data)

    def show_sentiment_trends(self, data):
        """
        Displays a sentiment trends chart.

        Args:
            data (pd.DataFrame): DataFrame containing the sentiment data.
        """
        st.subheader("Sentiment Trends")
        if "sentiment" in data.columns and "created_utc" in data.columns:
            fig, ax = plt.subplots()
            data["created_utc"] = pd.to_datetime(data["created_utc"], unit="s")
            data.sort_values("created_utc", inplace=True)
            ax.plot(data["created_utc"], data["sentiment"], marker="o")
            ax.set_title("Sentiment Trends Over Time")
            ax.set_xlabel("Time")
            ax.set_ylabel("Sentiment")
            st.pyplot(fig)
        else:
            st.warning("No sentiment data available to plot.")

    def run(self):
        """
        Runs the Streamlit dashboard.
        """
        st.title("Cryptocurrency Sentiment Dashboard")

        # Select Kafka Topic
        topic = st.selectbox("Select Kafka Topic", list(KAFKA_TOPICS.values()))
        consumer = self.get_kafka_consumer(topic)

        # Fetch and Display Data
        data = self.fetch_data(consumer, max_messages=500)
        st.write(f"Showing {len(data)} messages from topic '{topic}'")
        st.dataframe(data)

        # Show Sentiment Trends
        self.show_sentiment_trends(data)
