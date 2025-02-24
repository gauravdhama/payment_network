from flask import Blueprint, request, jsonify
import asyncio
import json

from app.utils.ignite_manager import get_transaction_features
from app.utils.model_manager import score_transaction

bp = Blueprint('score', __name__)

# Load rules from JSON file
with open('rules.json', 'r') as f:
    rules = json.load(f)

@bp.route('/', methods=['POST'])
async def score_api():
    try:
        # Get transaction data
        transaction_data = request.get_json()

        # Determine scoring flow (issuer or acquirer)
        scoring_flow = request.args.get('flow', 'issuer')  # Default to issuer flow

        # Apply rules
        rule_action = apply_rules(transaction_data)
        if rule_action == "block":
            return jsonify({"status": "blocked", "message": "Transaction blocked by rule"}), 403
        elif rule_action == "alert":
            # Send alert (replace with your actual alert mechanism)
            send_alert(transaction_data, rule)
            # Proceed with scoring (or take other action as needed)

        # Fetch or compute aggregate features from Apache Ignite
        transaction_features = await get_transaction_features(transaction_data)

        # Score the transaction using ONNX Runtime
        score = await score_transaction(transaction_features, scoring_flow)

        return jsonify({"status": "success", "score": score}), 200

    except asyncio.TimeoutError:
        # Handle timeout (return default or fallback behavior)
        return jsonify({"status": "timeout", "message": "ML scoring timeout"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def apply_rules(transaction_data):
    """
    Applies the rules to the transaction data and returns the action to take.
    """
    for rule in rules:
        conditions_met = all(
            eval(f"transaction_data.get('{condition['field']}') {condition['operator']} {condition['value']}")
            for condition in rule['conditions']
        )
        if conditions_met:
            return rule['action']

    return None  # No rule matched

def send_alert(transaction_data, rule):
    """
    Sends an alert for the matched rule to the issuer or acquirer.
    """
    try:
        # Determine recipient (issuer or acquirer) based on the rule or transaction data
        recipient = determine_alert_recipient(transaction_data, rule)  # You'll need to implement this function

        if recipient == "issuer":
            # Send alert to issuer (replace with your actual alert mechanism)
            send_alert_to_issuer(transaction_data, rule)
        elif recipient == "acquirer":
            # Send alert to acquirer (replace with your actual alert mechanism)
            send_alert_to_acquirer(transaction_data, rule)
        else:
            print("Invalid alert recipient")

    except Exception as e:
        print(f"Error sending alert: {e}")

def determine_alert_recipient(transaction_data, rule):
    """
    Determines the recipient of the alert (issuer or acquirer) based on the rule or transaction data.

    This is a placeholder function. You'll need to implement the logic to determine the recipient
    based on your specific requirements.
    """
    # TODO: Implement logic to determine alert recipient
    return "issuer"  # Placeholder: Default to issuer

def send_alert_to_issuer(transaction_data, rule):
    """
    Sends an alert to the issuer.

    This is a placeholder function. You'll need to implement the actual alert mechanism here,
    such as sending an email or using a message queue.
    """
    # TODO: Implement actual alert mechanism for issuer
    print(f"ALERT to issuer: Rule {rule['rule_id']} matched for transaction: {transaction_data}")

def send_alert_to_acquirer(transaction_data, rule):
    """
    Sends an alert to the acquirer.

    This is a placeholder function. You'll need to implement the actual alert mechanism here,
    such as sending an email or using a message queue.
    """
    # TODO: Implement actual alert mechanism for acquirer
    print(f"ALERT to acquirer: Rule {rule['rule_id']} matched for transaction: {transaction_data}")
