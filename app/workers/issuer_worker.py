import json
import pika
import requests
from app.utils.issuer_lookup import get_issuer_info

# --- Asynchronous routing to issuer using RabbitMQ with callback ---
def route_to_issuer_async(parsed_data, callback_url):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='issuer_queue')

    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())
    parsed_data['transaction_id'] = transaction_id

    # Publish message with transaction ID and callback URL
    channel.basic_publish(exchange='', routing_key='issuer_queue', body=json.dumps({
        'transaction_data': parsed_data,
        'callback_url': callback_url
    }))
    print(" [x] Sent transaction to issuer queue")
    connection.close()

    return {"status": "success", "message": "Transaction routed to issuer queue", "transaction_id": transaction_id}

# --- Worker process to handle issuer routing and callback ---
def issuer_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='issuer_queue')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        transaction_data = message['transaction_data']
        callback_url = message['callback_url']

        #... (process the transaction, including actual routing to issuer)...
        #... (use get_issuer_info and send HTTPS request as before)...

        # Send the issuer's response to the callback URL
        try:
            issuer_response = {'transaction_id': transaction_data['transaction_id'], 'status': 'approved'}  # Replace with actual response
            requests.post(callback_url, json=issuer_response)
        except requests.exceptions.RequestException as e:
            print(f"Error sending callback to acquirer: {e}")

        print(" [x] Processed transaction from issuer queue")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='issuer_queue', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
