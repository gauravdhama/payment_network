import json
import pika
from collections import defaultdict
import requests  # For sending data to settlement system

def send_to_clearing(transaction_id):
    """
    Sends a transaction to the clearing process.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='clearing_queue')

    # Fetch transaction details from the database (replace with your actual database query)
    transaction_details = {
        'transaction_id': transaction_id,
        #... (add other relevant transaction details)...
    }

    channel.basic_publish(exchange='', routing_key='clearing_queue', body=json.dumps(transaction_details))
    print(" [x] Sent transaction to clearing queue")
    connection.close()

def clearing_worker():
    """
    Worker process to handle clearing and settlement.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='clearing_queue')

    def callback(ch, method, properties, body):
        transaction_details = json.loads(body)

        #... (process the transaction for clearing)...
        #... (e.g., insert into cleared_transactions table)...

        # Group transactions by issuer and acquirer for settlement
        group_transactions_for_settlement()

        print(" [x] Processed transaction from clearing queue")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='clearing_queue', on_message_callback=callback)
    print(' [*] Waiting for messages in clearing queue. To exit press CTRL+C')
    channel.start_consuming()

def group_transactions_for_settlement():
    """
    Groups cleared transactions by issuer, acquirer, and currency, and generates a settlement file.
    """
    # Fetch cleared transactions from the database (replace with your actual database query)
    cleared_transactions = [
        #... (sample transactions)...
    ]

    # Group transactions by issuer, acquirer, and currency
    settlement_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'amount': 0, 'transactions':})))
    for transaction in cleared_transactions:
        issuer_id = transaction['issuer_id']
        acquirer_id = transaction['acquirer_id']
        amount = float(transaction['amount'])
        currency = transaction['currency']

        settlement_data[issuer_id][acquirer_id][currency]['amount'] += amount
        settlement_data[issuer_id][acquirer_id][currency]['transactions'].append(transaction['transaction_id'])

    # Add billing amounts and breakdown to settlement data
    for issuer_id, acquirer_data in settlement_data.items():
        for acquirer_id, currency_data in acquirer_data.items():
            for currency, data in currency_data.items():
                # Calculate billing amount for the issuer (replace with your actual logic)
                billing_amount, billing_code_breakdown = calculate_bill(issuer_id, start_date, end_date)
                data['billing_amount'] = billing_amount
                data['billing_code_breakdown'] = billing_code_breakdown
                data['total_amount'] = data['amount'] + billing_amount

    # Send settlement data to settlement system
    try:
        response = requests.post("http://settlement-system-api/settlement", json=settlement_data)  # Replace with actual settlement API endpoint
        response.raise_for_status()
        print("Settlement data sent to settlement system")
    except requests.exceptions.RequestException as e:
        print(f"Error sending settlement data to settlement system: {e}")
