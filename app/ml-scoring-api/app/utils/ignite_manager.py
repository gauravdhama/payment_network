import asyncio
import json
import pika  # Import pika for RabbitMQ

#... (other imports)...

async def get_transaction_features(transaction_data):
    """
    Fetches or computes aggregate features from Apache Ignite and sends them for persistence.
    """
    # Connect to Apache Ignite cluster
    #...

    # Extract relevant features from transaction_data
    #...

    # Fetch or compute aggregate features
    #...

    # Send features for asynchronous persistence
    send_features_for_persistence(transaction_features)

    return transaction_features

def send_features_for_persistence(features):
    """
    Sends features to a message queue for asynchronous persistence.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='feature_persistence_queue')

    channel.basic_publish(exchange='', routing_key='feature_persistence_queue', body=json.dumps(features))
    print(" [x] Sent features to feature_persistence_queue")
    connection.close()
