from flask import Flask

app = Flask(__name__)

# Import API modules
from app.api import settlement

# Register API blueprints
app.register_blueprint(settlement.bp, url_prefix='/api/settlement')

#... other initialization code if needed...

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')
