# Kafka, Postgres and Elasticsearch with Kafka Connect

This is a simple example of how to use Kafka Connect to stream data from Kafka to Postgres and Elasticsearch.
Postgres is still a work in progress.

## Pre-requisites
- Docker
- Docker Compose

Download the following plugins and place them in connect-plugins folder
- [Kafka Connector](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc)
- [Elasticsearch Connector](https://www.confluent.io/hub/confluentinc/kafka-connect-elasticsearch)

## Start
```
docker-compose up -d
```

## Elasticsearch Sink
```
curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d \
'{
  "name": "elasticsearch-sink",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "1",
    "topics": "example-topic",
    "key.ignore": "true",
    "schema.ignore": "true",
    "connection.url": "http://elastic:9200",
    "type.name": "_doc",
    "name": "elasticsearch-sink",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}'
```

## Postgres Sink [WIP]
```
curl -X POST http://localhost:8083/connectors -H 'Content-Type: application/json' -d \
'{
    "name": "jdbc-sink",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": 1,
        "topics": "test1",
        "connection.url": "jdbc:postgresql://pg-0:5432/meroxadb",
        "connection.user": "meroxauser",
        "connection.password": "meroxapass",
        "auto.create": true,
        "insert.mode": "upsert",
        "pk.mode": "none",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable": "false"
    }
}'
```


### Example producer
```
{"schema": {"type": "struct", "fields": [{"field": "name", "type": "string", "optional": false}]}, "data" : {"name": "test"}}
```