#/bin/bash

/bin/kafka-topics --create --topic $TEST_TOPIC_NAME --bootstrap-server kafka-1:9092
echo "topic $TEST_TOPIC_NAME was create"