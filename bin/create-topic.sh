#/bin/bash


# Wait for the Kafka broker to be ready
while ! nc -z kafka-1 9092; do   
  echo "Waiting for Kafka broker to be ready..."
  echo "Trying to creat topic $TEST_TOPIC_NAME"
  sleep 2
done

kafka-topics --create --topic orders --partitions 1 --replication-factor 1 --if-not-exists --bootstrap-server kafka-1:9092
echo "topic $TEST_TOPIC_NAME was created"