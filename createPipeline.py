'''
This file is used to create a pipeline for between kafka and (elastic search/Postgres)

Created on 02-Jun-2023
author: @vjspranav
'''

# Importing the required libraries
import argparse
import logging
import requests

# CONNECTOR_URL = "http://localhost:8083/connectors"

argparser = argparse.ArgumentParser()
# also add shorthands for the arguments
argparser.add_argument('-cu', '--connector_url', help='Connector url', default='http://localhost:8083/connectors')
argparser.add_argument('-cn', '--connector_name', help='Name of the connector', required=True)
argparser.add_argument('-t', '--topic', help='Name of the topic', required=True)
# elastic search url and port
argparser.add_argument('-eu', '--elastic_url', help='Elastic search url', default='localhost')
argparser.add_argument('-ep', '--elastic_port', help='Elastic search port', default='9200')
# postgres url and port
argparser.add_argument('-pu', '--postgres_url', help='Postgres url', default='localhost')
argparser.add_argument('-pp', '--postgres_port', help='Postgres port', default='5432')
argparser.add_argument('-pgu', '--postgres_user', help='Postgres user', default='meroxauser')
argparser.add_argument('-pgp', '--postgres_pass', help='Postgres password', default='meroxapass')
argparser.add_argument('-pgdb', '--postgres_db', help='Postgres database', default='meroxadb')

argparser.add_argument('-l', '--log', help='Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL', default='INFO')

args = argparser.parse_args()


# Logging configuration
logging.basicConfig(level=args.log.upper())

def create_elastic_connector(connector_url, connector_name, topic, elastic_url, elastic_port):
    '''
    This function is used to create a connector between kafka and elastic search
    '''
    logging.info("Creating Elastic Search connector")

    data = {
        "name": 'elasticsearch-' + connector_name,
        "config": {
            "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
            "tasks.max": "1",
            "topics": topic,
            "key.ignore": "true",
            "schema.ignore": "true",
            "connection.url": "http://" + elastic_url + ":" + elastic_port,
            "type.name": "_doc",
            "name": 'elasticsearch-' + connector_name,
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter.schemas.enable": "false"
        }
    }

    logging.debug(data)

    response = requests.post(connector_url, json=data)

    logging.debug(response.text)

    if response.status_code == 201:
        logging.info("Elastic Search connector created successfully")
    else:
        logging.error("Failed to create Elastic Search connector")
        logging.error(response.text)


def create_postgres_connector(connector_url, connector_name, topic, postgres_url, postgres_port):
    '''
    This function is used to create a connector between kafka and postgres
    '''
    logging.info("Creating Postgres connector")

    data = {
        "name": 'postgres-' + connector_name,
        "config": {
            "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
            "tasks.max": "1",
            "topics": topic,
            "connection.url": "jdbc:postgresql://" + postgres_url + ":" + postgres_port + "/" + args.postgres_db,
            "connection.user": args.postgres_user,
            "connection.password": args.postgres_pass,
            "auto.create": "true",
            "insert.mode": "insert",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "schemas.enable": "false",
            "pk.mode": "none"
        }
    }

    logging.debug(data)

    response = requests.post(connector_url, json=data)

    logging.debug(response.text)

    if response.status_code == 201:
        logging.info("Postgres connector created successfully")
    else:
        logging.error("Failed to create Postgres connector")
        logging.error(response.text)

if __name__ == '__main__':
    logging.info("Creating pipeline")

    create_elastic_connector(args.connector_url, args.connector_name, args.topic, args.elastic_url, args.elastic_port)
    create_postgres_connector(args.connector_url, args.connector_name, args.topic, args.postgres_url, args.postgres_port)

    logging.info("Pipeline created successfully")

    # Print saying that elastic data can be seen at http://elastic_url:elastic_port/topic/?pretty
    # Print saying that postgres data can be seen by connecting to postgres_url:postgres_port and using the credentials and table name will be topic name
    # pretty print the above

    print("Elastic data can be seen at http://" + args.elastic_url + ":" + args.elastic_port + "/" + args.topic + "/?pretty")
    print("Postgres data can be seen by connecting to " + args.postgres_url + ":" + args.postgres_port + " and using the credentials and table name will be " + args.topic)