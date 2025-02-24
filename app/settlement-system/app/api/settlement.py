from flask import Blueprint, request, jsonify
from app.utils.pdf_generator import generate_pdf_advisement
from app.utils.email_sender import send_email_advisement

bp = Blueprint('settlement', __name__)

@bp.route('/', methods=['POST'])
def settlement_api():
    try:
        settlement_data = request.get_json()

        # Process settlement data, generate PDF advisements, and send emails
        for issuer_id, acquirer_data in settlement_data.items():
            for acquirer_id, currency_data in acquirer_data.items():
                for currency, data in currency_data.items():
                    pdf_file = generate_pdf_advisement(issuer_id, acquirer_id, data['amount'], currency, data['transactions'], data.get('billing_code_breakdown', {}))
                    #... (retrieve email addresses for issuer and acquirer)...
                    send_email_advisement(issuer_email, pdf_file)
                    send_email_advisement(acquirer_email, pdf_file)

        return jsonify({"status": "success", "message": "Settlement data processed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
