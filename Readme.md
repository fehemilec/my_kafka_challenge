How to run this Kafka Project:

-- Possibility 1: Run using Function App as producer --

1. Start Function App in the folder src with command func start
2. Start Project with docker compose up
3. Start listenting with consumer to one of the brokers by running my_consumer.py module
4. Start producing events by sending Post Rest Api call to http://localhost:7071/api/order
5. Observe incoming events in consumer console

-- Possibility 2: Run using python modules only --

1. Start Project with docker compose up
3. Start listenting with consumer to one of the brokers by executing my_consumer.py module
4. Start producing events by by executing my_consumer.py module
5. Observe incoming events in consumer console
