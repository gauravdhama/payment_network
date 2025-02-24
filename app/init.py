from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Import API modules
from app.api import payment, callback

# Register API blueprints
app.register_blueprint(payment.bp, url_prefix='/api/payment')
app.register_blueprint(callback.bp, url_prefix='/api/payment/callback')

#... (other initialization code if needed)...

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
