from flask import Blueprint, request, jsonify

from app.workers.clearing_worker import send_to_clearing

bp = Blueprint('callback', __name__)

# Callback endpoint to receive issuer response
@bp.route('/', methods=['POST'])
def payment_callback():
    try:
        issuer_response = request.get_json()
        transaction_id = issuer_response['transaction_id']
        status = issuer_response['status']

        if status == 'approved':
            # Send the transaction to the clearing process
            send_to_clearing(transaction_id)

        #... (update transaction status in database, send response to acquirer, etc.)...

        return jsonify({"status": "success", "message": "Callback received"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
