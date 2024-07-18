#/bin/bash

# Wait for the Kafka broker to be ready
while ! nc -z kafka-1 9092; do   
  echo "Waiting for Kafka broker to be ready..."
  sleep 2
done

# Create the Kafka topic
kafka-topics --create --topic users --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server localhost:9092

echo "Kafka topic 'users' created"

# /bin/kafka-topics --create --topic $TEST_TOPIC_NAME --bootstrap-server localhost:9092
# echo "topic $TEST_TOPIC_NAME was create"