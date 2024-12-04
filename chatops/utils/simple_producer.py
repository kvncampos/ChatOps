from kafka import KafkaProducer
import time
import logging

logging.basicConfig(level=logging.DEBUG)


def send_messages():
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: v.encode("utf-8"),
        acks="all",
    )

    # Produce 100 messages
    topics = ["topic1", "topic2"]
    for topic in topics:
        for i in range(1, 50):
            message = f"Hello, Kafka! Message {i}"
            producer.send(topic, value=message)
            print(f"Message {i} sent to topic '{topic}': {message}")
            time.sleep(0.1)  # Add a slight delay to simulate traffic over time

    # Flush and close the producer
    producer.flush()
    producer.close()

    print("All messages sent!")


if __name__ == "__main__":
    send_messages()
