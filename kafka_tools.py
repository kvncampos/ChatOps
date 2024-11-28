from kafka.admin import KafkaAdminClient

admin_client = KafkaAdminClient(bootstrap_servers="kafka:9092")

# List topics
topics = admin_client.list_topics()
print("Kafka Topics:", topics)
