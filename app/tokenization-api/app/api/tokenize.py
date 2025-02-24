from flask import Blueprint, request, jsonify
from app.utils.token_manager import generate_token, detokenize

bp = Blueprint('tokenize', __name__)

@bp.route('/', methods=['POST'])
def tokenize_api():
    try:
        data = request.get_json()
        pan = data.get('pan')
        if not pan:
            return jsonify({"status": "error", "message": "Missing PAN"}), 400

        # Generate a token for the PAN
        token = generate_token(pan)
        return jsonify({"status": "success", "token": token}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bp.route('/detokenize', methods=['POST'])
def detokenize_api():
    try:
        data = request.get_json()
        token = data.get('token')
        if not token:
            return jsonify({"status": "error", "message": "Missing token"}), 400

        # Detokenize the token to get the PAN
        pan = detokenize(token)
        return jsonify({"status": "success", "pan": pan}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
