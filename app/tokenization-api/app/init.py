from flask import Flask

app = Flask(__name__)

# Import API modules
from app.api import tokenize

# Register API blueprints
app.register_blueprint(tokenize.bp, url_prefix='/api/tokenization')

#... other initialization code if needed...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Run on port 5002
