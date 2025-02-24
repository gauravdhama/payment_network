from flask import Blueprint, request, jsonify

from app.utils.three_d_secure import process_three_d_secure

bp = Blueprint('authentication', __name__)

@bp.route('/', methods=['POST'])
def authentication_api():
    try:
        transaction_data = request.get_json()

        # Extract 3-D Secure fields
        cavv = transaction_data.get('CAVV')
        eci = transaction_data.get('ECI')
        xid = transaction_data.get('XID')

        # Perform 3-D Secure authentication
        authentication_result = process_three_d_secure(cavv, eci, xid)

        if authentication_result:
            return jsonify({"status": "success", "message": "3-D Secure authentication successful"}), 200
        else:
            return jsonify({"status": "error", "message": "3-D Secure authentication failed"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
