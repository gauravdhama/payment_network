from flask import Flask

app = Flask(__name__)

# Import API modules
from app.api import authentication

# Register API blueprints
app.register_blueprint(authentication.bp, url_prefix='/api/3ds')

#... other initialization code if needed...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)  # Run on port 5004
