from flask import Blueprint, request, jsonify
from aiohttp import ClientSession
import asyncio
from openexchangerates import OpenExchangeRatesClient

from app.utils.vault import get_secret
from app.utils.hsm import encrypt_with_hsm
from app.utils.iso8586 import parse_iso8586_message
from app.workers.issuer_worker import route_to_issuer_async
from app.utils.splunk_logger import log_to_splunk

bp = Blueprint('payment', __name__)

# OAuth 2.0 configuration (replace with your actual OAuth provider details)
#... (OAuth configuration using secrets from Vault)...

# API endpoint to process payments with pessimistic locking
@bp.route('/', methods=['POST'])
async def process_payment():
    # OAuth 2.0 authentication
    if 'Authorization' not in request.headers:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    async with ClientSession() as session:
        try:
            # Fetch access token from Authorization header
            token = request.headers['Authorization'].split(' ')
            resp = oauth.acquire_token('acquirer_oauth', token=token)

            # Verify access token
            if not resp or 'access_token' not in resp:
                return jsonify({"status": "error", "message": "Invalid access token"}), 401

            # Access token is valid, proceed with payment processing
            iso_message = request.data.decode('utf-8')
            parsed_data = parse_iso8586_message(iso_message)
            pan = parsed_data.get("PAN")

            # --- Pessimistic locking ---
            conn = await psycopg2.connect("your_database_connection_string")
            async with conn.cursor() as cur:
                # Acquire a lock on the transaction row
                await cur.execute("SELECT * FROM transactions WHERE id = %s FOR UPDATE", (transaction_id,))
                row = await cur.fetchone()
                if not row:
                    return jsonify({"status": "error", "message": "Transaction not found"}), 404

                # --- Encrypt PAN using HSM ---
                encrypted_pan = encrypt_with_hsm(pan)

                # Store encrypted PAN and other data
                await cur.execute("INSERT INTO transactions (..., pan,...) VALUES (..., %s,...)",
                            (..., encrypted_pan,...))

                # --- Route to issuer asynchronously with callback ---
                callback_url = request.base_url + "/callback"
                routing_result = route_to_issuer_async(parsed_data, callback_url)

                # Update the transaction status
                await cur.execute("UPDATE transactions SET status = %s, status_updated_at = NOW() WHERE id = %s", ("authorized", transaction_id))

                # Log transaction history
                await cur.execute("INSERT INTO transaction_history (transaction_id, status) VALUES (%s, %s)", (transaction_id, "authorized"))

            await conn.commit()
            await conn.close()

            # Currency conversion
            client = OpenExchangeRatesClient('YOUR_APP_ID')  # Replace with your actual App ID
            latest = client.latest()
            exchange_rate = latest.rates.get(parsed_data.get('currency'))
            if exchange_rate:
                converted_amount = float(parsed_data.get('amount')) * exchange_rate
                #... (store original and converted amounts in the database)...

            # Log payment request
            log_to_splunk({
                "event": "payment_request_received",
                "transaction_id": transaction_id,
                "amount": parsed_data.get("amount"),
                "currency": parsed_data.get("currency")
            })

            return jsonify(routing_result), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/<transaction_id>/history', methods=['GET'])
async def get_transaction_history(transaction_id):
    try:
        conn = await psycopg2.connect("your_database_connection_string")
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM transaction_history WHERE transaction_id = %s", (transaction_id,))
            history = await cur.fetchall()
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/<transaction_id>/refund', methods=['POST'])
async def refund_transaction(transaction_id):
    try:
        #... (validate request and authenticate user)...

        conn = await psycopg2.connect("your_database_connection_string")
        async with conn.cursor() as cur:
            # Update transaction status
            await cur.execute("UPDATE transactions SET status = %s, status_updated_at = NOW() WHERE id = %s", ("refunded", transaction_id))

            # Log transaction history
            await cur.execute("INSERT INTO transaction_history (transaction_id, status) VALUES (%s, %s)", (transaction_id, "refunded"))

        #... (initiate refund process with issuer and acquirer)...

        return jsonify({"status": "success", "message": "Refund initiated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/<transaction_id>/chargeback', methods=['POST'])
async def chargeback_transaction(transaction_id):
    try:
        #... (validate request and authenticate user)...

        conn = await psycopg2.connect("your_database_connection_string")
        async with conn.cursor() as cur:
            # Update transaction status
            await cur.execute("UPDATE transactions SET status = %s, status_updated_at = NOW() WHERE id = %s", ("charged_back", transaction_id))

            # Log transaction history
            await cur.execute("INSERT INTO transaction_history (transaction_id, status) VALUES (%s, %s)", (transaction_id, "charged_back"))

        #... (initiate chargeback process with issuer and acquirer)...

        return jsonify({"status": "success", "message": "Chargeback initiated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
